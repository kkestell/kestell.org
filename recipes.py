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
                 instruction_groups: List[InstructionGroup]):
        self.title = title
        self.description = description
        self.ingredient_groups = ingredient_groups
        self.instruction_groups = instruction_groups

    def to_dict(self):
        return {
            'title': self.title,
            'description': self.description,
            'ingredient_groups': [ig.__dict__ for ig in self.ingredient_groups],
            'instruction_groups': [ig.__dict__ for ig in self.instruction_groups]
        }


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

        return RecipeModel(title, description, ingredient_groups, instruction_groups)

    def parse_ingredient_groups(self, root, start_index) -> Optional[List[IngredientGroup]]:
        groups = []
        current_index = start_index

        while current_index < len(root) and root[current_index].tag != 'h2':
            if root[current_index].tag == 'h3':
                title = root[current_index].text
                current_index += 1
                if len(root) <= current_index or root[current_index].tag != 'ul':
                    return None
                ingredients = [li.text for li in root[current_index] if li.tag == 'li']
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
                instructions = [li.text for li in root[current_index] if li.tag == 'li']
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
