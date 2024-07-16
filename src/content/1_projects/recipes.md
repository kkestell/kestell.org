---
title: Recipes
date: 2024-07-14
draft: false
---

## File Formats

### JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["title", "ingredient_groups"],
  "properties": {
    "title": {
      "type": "string"
    },
    "description": {
      "type": "string"
    },
    "ingredient_groups": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": ["ingredients"],
        "properties": {
          "title": {
            "type": "string"
          },
          "ingredients": {
            "type": "array",
            "minItems": 1,
            "items": {
              "type": "string"
            }
          }
        }
      }
    },
    "instruction_groups": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["instructions"],
        "properties": {
          "title": {
            "type": "string"
          },
          "instructions": {
            "type": "array",
            "items": {
              "type": "string"
            }
          }
        }
      }
    }
  }
}
```

### JSON Example

```json
{
  "title": "Chocolate Cake with Vanilla Frosting",
  "description": "A classic chocolate cake with vanilla frosting.",
  "ingredient_groups": [
    {
      "title": "For the Cake",
      "ingredients": [
        "1 3/4 cups all-purpose flour",
        "1 1/2 cups granulated sugar",
        "3/4 cup unsweetened cocoa powder",
        "1 1/2 teaspoons baking powder",
        "1 1/2 teaspoons baking soda",
        "1 teaspoon salt",
        "2 large eggs",
        "1 cup whole milk",
        "1/2 cup vegetable oil",
        "2 teaspoons vanilla extract",
        "1 cup boiling water"
      ]
    },
    {
      "title": "For the Frosting",
      "ingredients": [
        "1 cup unsalted butter, softened",
        "4 cups powdered sugar",
        "2 teaspoons vanilla extract",
        "2-4 tablespoons milk"
      ]
    }
  ],
  "instruction_groups": [
    {
      "title": "Making the Cake",
      "instructions": [
        "Preheat oven to 350°F.",
        "Grease and flour two 9-inch round baking pans.",
        "In a large bowl, combine flour, sugar, cocoa, baking powder, baking soda, and salt.",
        "Add eggs, milk, oil, and vanilla; beat on medium speed for 2 minutes.",
        "Stir in boiling water (batter will be thin).",
        "Pour batter into prepared pans.",
        "Bake for 30-35 minutes or until a toothpick inserted in the center comes out clean.",
        "Cool in pans for 10 minutes, then remove from pans and cool completely on wire racks."
      ]
    },
    {
      "title": "Making the Frosting",
      "instructions": [
        "In a large bowl, beat butter until creamy.",
        "Gradually add powdered sugar, beating until smooth.",
        "Beat in vanilla.",
        "Add milk, 1 tablespoon at a time, until desired consistency is reached."
      ]
    }
  ]
}
```

### Markdown

```markdown
# Chocolate Cake with Vanilla Frosting

A classic chocolate cake with vanilla frosting.

## Ingredients

### For the Cake

- 1 3/4 cups all-purpose flour
- 1 1/2 cups granulated sugar
- 3/4 cup unsweetened cocoa powder
- 1 1/2 teaspoons baking powder
- 1 1/2 teaspoons baking soda
- 1 teaspoon salt
- 2 large eggs
- 1 cup whole milk
- 1/2 cup vegetable oil
- 2 teaspoons vanilla extract
- 1 cup boiling water

### For the Frosting

- 1 cup unsalted butter, softened
- 4 cups powdered sugar
- 2 teaspoons vanilla extract
- 2-4 tablespoons milk

## Instructions

### Making the Cake

1. Preheat oven to 350°F.
2. Grease and flour two 9-inch round baking pans.
3. In a large bowl, combine flour, sugar, cocoa, baking powder, baking soda, and salt.
4. Add eggs, milk, oil, and vanilla; beat on medium speed for 2 minutes.
5. Stir in boiling water (batter will be thin).
6. Pour batter into prepared pans.
7. Bake for 30-35 minutes or until a toothpick inserted in the center comes out clean.
8. Cool in pans for 10 minutes, then remove from pans and cool completely on wire racks.

### Making the Frosting

1. In a large bowl, beat butter until creamy.
2. Gradually add powdered sugar, beating until smooth.
3. Beat in vanilla.
4. Add milk, 1 tablespoon at a time, until desired consistency is reached.
```
