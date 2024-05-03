---
title: XeTeX
date: 2024-04-03
draft: false
---

## Recipes

[Download PDF](/static/images/xetex/recipe.pdf)

![Recipe](/static/images/xetex/recipe.jpg)

```
\documentclass[11pt]{article}
\usepackage{fontspec}
\usepackage{geometry}
\usepackage{enumitem}
\usepackage{graphicx}
\usepackage{paracol}
\usepackage{microtype}
\geometry{letterpaper, margin=0.75in}
\setmainfont{Source Sans 3}
\newfontfamily\headingfont{Source Sans 3}
\pagestyle{empty}
\begin{document}
\begin{center}
    {\Huge \bfseries \headingfont Chocolate Cake}
\end{center}
\vspace{1em}
For cupcakes, bake at 350°F for 25 minutes. For 6” cakes, adjust the baking time as needed, typically baking at 350°F.
\vspace{1em}
\begin{paracol}{2}
\section*{Ingredients}
\subsection*{For the Cake}
\begin{tabular}{@{}ll}
400g & Sugar \\
180g & All-Purpose Flour \\
65g & Unsweetened Cocoa Powder \\
1 1⁄2 tsp & Baking Powder \\
1 1⁄2 tsp & Baking Soda \\
1 tsp & Salt \\
2 tsp & Espresso Powder \\
2 ea & Eggs \\
1 cup & Milk \\
1⁄2 cup & Vegetable Oil \\
2 tsp & Vanilla Extract \\
1 cup & Boiling Water \\
\end{tabular}
\subsection*{For the Frosting}
\begin{tabular}{@{}ll}
1 cup & Butter, Softened \\
100 g & Unsweetened Cocoa Powder \\
575 g & Powdered Sugar \\
1⁄2 cup & Milk \\
2 tsp & Vanilla Extract \\
\end{tabular}
\switchcolumn
\section*{Instructions}
\subsection*{For the Cake}
\begin{enumerate}[leftmargin=*]
    \item Preheat oven to 350°F. Spray a bundt cake pan with cooking spray.
    \item In a large mixing bowl, combine the sugar, flour, cocoa powder, baking powder, baking soda, and salt.
    \item Make a well in the middle of the dry ingredients and add in the eggs, milk, vegetable oil, and vanilla extract. Beat for 2 minutes at medium speed, then stir in the boiling water with espresso powder.
    \item Pour the batter into the prepared bundt pan. Bake for 35-45 minutes or until a toothpick comes out clean. Let the cake cool in the pan for 10 minutes, then flip it out onto a wire rack and let cool completely before assembling.
\end{enumerate}
\subsection*{For the Frosting}
\begin{enumerate}[leftmargin=*]
    \item In a large mixing bowl, beat the butter until light and fluffy. Add in the cocoa powder and powdered sugar, mixing until combined.
    \item Add in the milk and vanilla extract, beating until smooth and creamy. If the frosting is too thick, add more milk, 1 tablespoon at a time, until the desired consistency is reached.
    \item Frost the cooled cake as desired.
\end{enumerate}
\end{paracol}
\vspace{1em}
\section*{Notes}
For cupcakes, bake at 350°F for 25 minutes. For 6” cakes, adjust the baking time as needed, typically baking at 350°F.
\end{document}
```

## Notes

Compile with XeLaTeX:

```
xelatex example.tex
```

Convert PDF to JPG:

```
convert -density 70 -quality 100 -flatten example.pdf example.jpg
```

Add drop shadow:

```
convert example.jpg \( +clone -background black -shadow 20x4+0+0 \) +swap -background white -layers merge +repage example_shadow.jpg
```