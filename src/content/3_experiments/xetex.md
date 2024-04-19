---
title: XeTeX
date: 2024-04-03
draft: false
---

## Recipes

![Recipe](/static/images/xetex/recipe.jpg)

```
\documentclass[11pt]{article}
\usepackage{fontspec}
\usepackage{geometry}
\usepackage{titlesec}
\usepackage{enumitem}
\usepackage{graphicx}
\usepackage{paracol}
\usepackage{microtype}
\geometry{letterpaper, margin=0.75in}
\setmainfont{Latin Modern Sans}
\newfontfamily\headingfont{EB Garamond}
\titleformat*{\section}{\Large\headingfont}
\titleformat*{\subsection}{\large\headingfont}
\titleformat*{\subsubsection}{\normalsize\headingfont}
\pagestyle{empty}
\begin{document}
\begin{center}
    {\Large \bfseries \headingfont Chocolate Cake}
\end{center}
\vspace{1em}
For cupcakes, bake at 350°F for 25 minutes. For 6” cakes, adjust the baking time as needed, typically baking at 350°F.
\vspace{1em}
\begin{paracol}{2}
\section*{Ingredients}
\subsection*{For the Cake}
\begin{itemize}[noitemsep]
    \item 2 cups white sugar (396g)
    \item 1 3/4 cups all-purpose flour (180g)
    \item 3/4 cup unsweetened cocoa powder (63g)
    \item 1 1/2 teaspoons baking powder
    \item 1 1/2 teaspoons baking soda
    \item 1 teaspoon salt
    \item 2 teaspoons espresso powder
    \item 2 eggs
    \item 1 cup milk
    \item 1/2 cup vegetable oil
    \item 2 teaspoons vanilla extract
    \item 1 cup boiling water
\end{itemize}
\switchcolumn
\section*{Instructions}
\subsection*{For the Cake}
\begin{enumerate}
    \item Preheat oven to 350°F. Spray a bundt cake pan with cooking spray.
    \item In a large mixing bowl, combine the sugar, flour, cocoa powder, baking powder, baking soda, and salt.
    \item Make a well in the middle of the dry ingredients and add in the eggs, milk, vegetable oil, and vanilla extract. Beat for 2 minutes at medium speed, then stir in the boiling water with espresso powder.
    \item Pour the batter into the prepared bundt pan. Bake for 35-45 minutes or until a toothpick comes out clean. Let the cake cool in the pan for 10 minutes, then flip it out onto a wire rack and let cool completely before assembling.
\end{enumerate}
\end{paracol}
\vspace{1em}
\section*{Notes}
For cupcakes, bake at 350°F for 25 minutes. For 6” cakes, adjust the baking time as needed, typically baking at 350°F.
\end{document}
```
