import re
from typing import List, Optional

import markdown
from markdown import Extension
from markdown.treeprocessors import Treeprocessor


class IngredientGroup:
    def __init__(self, title: str, ingredients: List[str]):
        self.title = title
        self.ingredients = ingredients


class InstructionGroup:
    def __init__(self, title: str, instructions: List[str]):
        self.title = title
        self.instructions = instructions


class RecipeModel:
    def __init__(self, title: str, description: Optional[str], ingredient_groups: List[IngredientGroup],
                 instruction_groups: List[InstructionGroup], notes: Optional[str] = None):
        self.title = title
        self.description = description
        self.ingredient_groups = ingredient_groups
        self.instruction_groups = instruction_groups
        self.notes = notes


def normalize_fractions(val):
    return re.sub(r'(\d+)/(\d+)', r'\1⁄\2', val)


class RecipeParser(Treeprocessor):
    def run(self, root):
        self.recipe = self.parse_recipe(root)
        if self.recipe is None:
            raise ValueError("Markdown structure does not conform to expected format")
        return root  # We still need to return the root for other processors

    def parse_recipe(self, root) -> Optional[RecipeModel]:
        if len(root) == 0 or root[0].tag != 'h1':
            return None

        title = root[0].text
        current_index = 1
        description = None

        if len(root) > current_index and root[current_index].tag == 'p':
            description = root[current_index].text
            current_index += 1

        if len(root) <= current_index or root[current_index].tag != 'h2' or root[current_index].text != 'Ingredients':
            return None

        current_index += 1
        ingredient_groups = self.parse_ingredient_groups(root, current_index)
        if ingredient_groups is None:
            return None

        # Find the Instructions heading
        while current_index < len(root) and (root[current_index].tag != 'h2' or root[current_index].text != 'Instructions'):
            current_index += 1

        if current_index >= len(root):
            return None

        current_index += 1
        instruction_groups = self.parse_instruction_groups(root, current_index)
        if instruction_groups is None:
            return None

        current_index += 1
        notes = None
        if current_index < len(root) and root[current_index].tag == 'h2' and root[current_index].text == 'Notes':
            notes = root[current_index + 1].text
            current_index += 2

        return RecipeModel(title, description, ingredient_groups, instruction_groups, notes)

    def parse_ingredient_groups(self, root, start_index) -> Optional[List[IngredientGroup]]:
        groups = []
        current_index = start_index

        while current_index < len(root) and root[current_index].tag != 'h2':
            if root[current_index].tag == 'h3':
                title = root[current_index].text
                current_index += 1
                if len(root) <= current_index or root[current_index].tag != 'ul':
                    return None
                ingredients = [normalize_fractions(li.text) for li in root[current_index] if li.tag == 'li']
                groups.append(IngredientGroup(title, ingredients))
                current_index += 1
            elif root[current_index].tag == 'ul':
                ingredients = [normalize_fractions(li.text) for li in root[current_index] if li.tag == 'li']
                groups.append(IngredientGroup("", ingredients))
                current_index += 1
            else:
                current_index += 1

        return groups if groups else None

    def parse_instruction_groups(self, root, start_index) -> Optional[List[InstructionGroup]]:
        groups = []
        current_index = start_index

        while current_index < len(root):
            if root[current_index].tag == 'h3':
                title = root[current_index].text
                current_index += 1
                if len(root) <= current_index or root[current_index].tag != 'ol':
                    return None
                instructions = [normalize_fractions(li.text) for li in root[current_index] if li.tag == 'li']
                groups.append(InstructionGroup(title, instructions))
                current_index += 1
            elif root[current_index].tag == 'ol':
                instructions = [normalize_fractions(li.text) for li in root[current_index] if li.tag == 'li']
                groups.append(InstructionGroup("", instructions))
                current_index += 1
            else:
                break

        return groups if groups else None


class RecipeExtension(Extension):
    def __init__(self):
        self.recipe_parser = None
        super().__init__()

    def extendMarkdown(self, md):
        self.recipe_parser = RecipeParser(md)
        md.treeprocessors.register(self.recipe_parser, 'recipeparser', 15)


def parse_recipe_markdown(content: str) -> Optional[RecipeModel]:
    recipe_extension = RecipeExtension()
    md = markdown.Markdown(extensions=[recipe_extension])

    try:
        _ = md.convert(content)
        recipe = recipe_extension.recipe_parser.recipe
        if recipe:
            return recipe
        else:
            return None
    except ValueError as e:
        print(f"Failed to parse recipe: {str(e)}")
        return None


def _escape_latex(text):
    mapping = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\^{}',
        '\\': r'\textbackslash{}',
        '<': r'\textless{}',
        '>': r'\textgreater{}'
    }
    return "".join(mapping.get(c, c) for c in text)


def recipe_to_latex(recipe: RecipeModel) -> str:
    title = recipe.title
    description = recipe.description
    ingredient_groups = recipe.ingredient_groups
    instruction_groups = recipe.instruction_groups
    notes = recipe.notes
    reviews = None
    source = None
    source_latex = "\\fancyfoot[C]{\\footnotesize " + _escape_latex(source) + "}" if source else ""

    latex = [
        "\\documentclass[10pt]{article}",
        "\\usepackage{fontspec}",
        "\\usepackage{geometry}",
        "\\usepackage{enumitem}",
        "\\usepackage{graphicx}",
        "\\usepackage{paracol}",
        "\\usepackage{microtype}",
        "\\usepackage{parskip}",
        "\\usepackage{fancyhdr}",
        "\\geometry{letterpaper, margin=0.75in}",
        "\\setmainfont{Source Serif 4}",
        "\\newfontfamily\\headingfont{Source Serif 4}",
        "\\pagestyle{fancy}",
        "\\fancyhf{}",
        "\\renewcommand{\\headrulewidth}{0pt}",
        source_latex,
        "\\begin{document}",
        "\\setlist[enumerate,1]{itemsep=0em}",
        "\\begin{center}",
        "{\\huge \\bfseries \\headingfont " + _escape_latex(title) + "}",
        "\\end{center}",
        "\\vspace{1em}"
    ]

    if description:
        latex.append("\\noindent " + _escape_latex(description))

    latex.append("\\vspace{1em}")
    latex.append("\\columnratio{0.35}")  # Adjust the column ratio as needed
    latex.append("\\begin{paracol}{2}")
    latex.append("\\section*{Ingredients}")
    latex.append("\\raggedright")

    for ingredient_group in ingredient_groups:
        if ingredient_group.title:
            latex.append(f"\\subsection*{{{_escape_latex(ingredient_group.title)}}}")
        latex.append("\\begin{itemize}[leftmargin=*]")
        for ingredient in ingredient_group.ingredients:
            latex.append(f"\\item {_escape_latex(ingredient)}")
        latex.append("\\end{itemize}")

    latex.append("\\switchcolumn")
    latex.append("\\section*{Instructions}")

    for instruction_group in instruction_groups:
        if instruction_group.title:
            latex.append(f"\\subsection*{{{_escape_latex(instruction_group.title)}}}")
        latex.append("\\begin{enumerate}[leftmargin=*]")
        for instruction in instruction_group.instructions:
            latex.append(f"\\item {_escape_latex(instruction)}")
        latex.append("\\end{enumerate}")

    latex.append("\\end{paracol}")

    if notes:
        latex.append("\\section*{Notes}")
        latex.append(_escape_latex(notes))

    if reviews:
        latex.append("\\section*{Tips}")
        for review in reviews:
            latex.append(_escape_latex(review))
            latex.append("\\par")

    latex.append("\\end{document}")

    return "\n".join(latex)
