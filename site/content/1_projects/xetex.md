---
title: XeTeX
date: 2024-04-03
draft: false
---

## Recipes

![Recipe](/static/images/xetex/recipe.png)

```
\documentclass[10pt]{article}
\usepackage{fontspec}
\usepackage{geometry}
\usepackage{enumitem}
\usepackage{graphicx}
\usepackage{paracol}
\usepackage{microtype}
\usepackage{parskip}
\usepackage{fancyhdr}
\geometry{letterpaper, margin=0.75in}
\setmainfont{Source Serif 4}
\newfontfamily\headingfont{Source Serif 4}
\pagestyle{fancy}
\fancyhf{}
\renewcommand{\headrulewidth}{0pt}
\fancyfoot[C]{\footnotesize https://www.allrecipes.com/recipe/17644/german-chocolate-cake-iii/}
\begin{document}
\setlist[enumerate,1]{itemsep=0em}
\begin{center}
{\huge \bfseries \headingfont German Chocolate Cake III}
\end{center}
\vspace{1em}
\vspace{1em}
\columnratio{0.35}
\begin{paracol}{2}
\section*{Ingredients}
\raggedright
\subsection*{For the Cake}
\begin{itemize}[leftmargin=*]
\item 1⁄2 cup water
\item 4 (1 ounce) squares German sweet chocolate
\item 1 cup butter, softened
\item 2 cups white sugar
\item 4 egg yolks
\item 1 teaspoon vanilla extract
\item 1 cup buttermilk
\item 2 1⁄2 cups cake flour
\item 1 teaspoon baking soda
\item 1⁄2 teaspoon salt
\item 4 egg whites
\item 1 cup white sugar
\end{itemize}
\subsection*{For the Filling}
\begin{itemize}[leftmargin=*]
\item 1 cup evaporated milk
\item 1⁄2 cup butter
\item 3 egg yolks, beaten
\item 1 1⁄3 cups flaked coconut
\item 1 cup chopped pecans
\item 1 teaspoon vanilla extract
\item 1⁄2 teaspoon shortening
\item 1 (1 ounce) square semisweet chocolate
\end{itemize}
\switchcolumn
\section*{Instructions}
\subsection*{Making the Cake}
\begin{enumerate}[leftmargin=*]
\item Preheat oven to 350°F (175°C). Grease and flour three 9-inch round pans.
\item Sift together the cake flour, baking soda, and salt. Set aside.
\item Heat water and 4 ounces of chocolate in a small saucepan until melted. Remove from heat and let cool.
\item Cream together 1 cup butter and 2 cups sugar until light and fluffy. Beat in 4 egg yolks one at a time.
\item Blend in the cooled chocolate mixture and vanilla extract.
\item Gradually add the flour mixture to the butter mixture, alternating with the buttermilk, mixing until just combined.
\item Beat egg whites until stiff peaks form.
\item Gently fold one-third of the beaten egg whites into the batter. Then quickly fold in the remaining egg whites until no streaks remain.
\item Pour batter into the prepared pans.
\item Bake for 30 minutes, or until a toothpick inserted into the center comes out clean.
\item Let cakes cool in the pans for 10 minutes before inverting onto a wire rack to cool completely.
\end{enumerate}
\subsection*{Preparing the Filling}
\begin{enumerate}[leftmargin=*]
\item Combine evaporated milk, 1 cup sugar, 1/2 cup butter, and 3 egg yolks in a saucepan. Cook over low heat, stirring constantly, until thickened.
\item Remove from heat. Stir in coconut, pecans, and vanilla extract.
\item Let filling cool until thick enough to spread.
\end{enumerate}
\subsection*{Creating the Frosting}
\begin{enumerate}[leftmargin=*]
\item Melt shortening and 1 ounce of chocolate in a small saucepan. Stir until smooth. Drizzle over cooled cake layers.
\end{enumerate}
\end{paracol}
\end{document}
```

## Notes

Compile with XeLaTeX:

```
xelatex recipe.tex
```

Convert to PNG and add a drop shadow:

`20x4+0+0` is 20% opacity, 4px sigma (blur amount), 0 horizontal offset, 0 vertical offset.

```
convert -density 300 recipe.pdf -background white -flatten -alpha off miff:- | \
convert - \( +clone -background black -shadow 20x4+0+0 \) +swap -background none -layers merge +repage recipe.png
```