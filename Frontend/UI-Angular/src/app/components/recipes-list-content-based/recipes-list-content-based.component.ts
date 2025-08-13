import { Component, Input, OnInit, input } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { RecipesService } from '../../services/recipes.service';
import { Location } from '@angular/common'; // Import the Location class from '@angular/common'
import { ProgressSpinnerMode } from '@angular/material/progress-spinner';

@Component({
  selector: 'app-recipes-list-content-based',
  templateUrl: './recipes-list-content-based.component.html',
  styleUrl: './recipes-list-content-based.component.css'
})
export class RecipesListContentBasedComponent implements OnInit{
  recipe: any;
  user_id:  string = "6678f64d68c8b09fe477b57d";
  recipesList: any = [];
  mode: ProgressSpinnerMode = 'indeterminate';
  value = 50;
  showSpinner: boolean = true;
//   contentBasedRecipes: any = [
//     {
//         "algorithm": "collaborative_item_based",
//         "description": "this recipe is posted by request and was originaly from chef sam choy's cookbook ",
//         "id": "64f5b522b5997a1d1052aa08",
//         "ingredients": [
//             "pork spareribs",
//             "soy sauce",
//             "fresh garlic",
//             "fresh ginger",
//             "chili powder",
//             "fresh coarse ground black pepper",
//             "salt",
//             "fresh cilantro leaves",
//             "tomato sauce",
//             "brown sugar",
//             "yellow onion",
//             "white vinegar",
//             "honey",
//             "a.1. original sauce",
//             "liquid smoke",
//             "cracked black pepper",
//             "cumin",
//             "dry mustard",
//             "cinnamon sticks",
//             "orange, juice of",
//             "mirin",
//             "water"
//         ],
//         "minutes": 120,
//         "n_ingredients": "22",
//         "n_steps": "10",
//         "name": "backyard style  barbecued ribs",
//         "nutrition": [
//             1109.5,
//             83.0,
//             378.0,
//             275.0,
//             96.0,
//             86.0,
//             36.0
//         ],
//         "steps": [
//             "in a medium saucepan combine all the ingredients for sauce#1 , bring to a full rolling boil , reduce heat to medium low and simmer for 1 hour , stirring often",
//             "rub the ribs with soy sauce , garlic , ginger , chili powder , pepper , salt and chopped cilantro , both sides !",
//             "wrap ribs in heavy duty foil",
//             "let stand 1 hour",
//             "preheat oven to 350 degrees",
//             "place ribs in oven for 1 hour , turning once after 30 minutes",
//             "3 times during cooking the ribs open foil wrap and drizzle ribs with sauce#1",
//             "place all the ingredients for sauce#2 in a glass or plastic bowl , whisk well and set aside",
//             "remove ribs from oven and place on serving platter",
//             "offer both sauces at table to drizzle over ribs"
//         ],
//         "submitted": "2003-07-30",
//         "tags": [
//             "weeknight",
//             "time-to-make",
//             "course",
//             "main-ingredient",
//             "cuisine",
//             "preparation",
//             "occasion",
//             "north-american",
//             "south-west-pacific",
//             "main-dish",
//             "pork",
//             "oven",
//             "holiday-event",
//             "stove-top",
//             "hawaiian",
//             "spicy",
//             "copycat",
//             "independence-day",
//             "meat",
//             "pork-ribs",
//             "super-bowl",
//             "novelty",
//             "taste-mood",
//             "savory",
//             "sweet",
//             "equipment",
//             "4-hours-or-less"
//         ]
//     },
//     {
//         "algorithm": "collaborative_item_based",
//         "description": "this is a super easy, great tasting, make ahead side dish that looks like you spent a lot more time preparing than you actually do. plus, most everything is done in advance. the times do not reflect the standing time of the potatoes.",
//         "id": "64f5b522b5997a1d1052aa04",
//         "ingredients": [
//             "spreadable cheese with garlic and herbs",
//             "new potatoes",
//             "shallots",
//             "parsley",
//             "tarragon",
//             "olive oil",
//             "red wine vinegar",
//             "salt",
//             "pepper",
//             "red bell pepper",
//             "yellow bell pepper"
//         ],
//         "minutes": 45,
//         "n_ingredients": "11",
//         "n_steps": "11",
//         "name": "alouette  potatoes",
//         "nutrition": [
//             368.1,
//             17.0,
//             10.0,
//             2.0,
//             14.0,
//             8.0,
//             20.0
//         ],
//         "steps": [
//             "place potatoes in a large pot of lightly salted water and bring to a gentle boil",
//             "cook until potatoes are just tender",
//             "drain",
//             "place potatoes in a large bowl and add all ingredients except the\"alouette\"",
//             "mix well and transfer to a buttered 8x8 inch glass baking dish with 2 inch sides",
//             "press the potatoes with a spatula to make top as flat as possible",
//             "set aside for 2 hours at room temperature",
//             "preheat oven to 350^f",
//             "spread\"alouette\" evenly over potatoes and bake 15 minutes",
//             "divide between plates",
//             "garnish with finely diced red and yellow bell peppers"
//         ],
//         "submitted": "2003-04-14",
//         "tags": [
//             "60-minutes-or-less",
//             "time-to-make",
//             "course",
//             "main-ingredient",
//             "preparation",
//             "occasion",
//             "side-dishes",
//             "eggs-dairy",
//             "potatoes",
//             "vegetables",
//             "oven",
//             "easy",
//             "dinner-party",
//             "holiday-event",
//             "easter",
//             "cheese",
//             "stove-top",
//             "dietary",
//             "christmas",
//             "new-years",
//             "thanksgiving",
//             "independence-day",
//             "st-patricks-day",
//             "valentines-day",
//             "inexpensive",
//             "brunch",
//             "superbowl",
//             "equipment",
//             "presentation",
//             "served-hot"
//         ]
//     },
//     {
//         "algorithm": "collaborative_item_based",
//         "description": "i'd have to say that this is a labor of love dish, but i give you my word that this recipe is better than bush's. enjoy! oh, and also this recipe is easily doubled. in fact, i think it turns out better when it is.",
//         "id": "64f5b522b5997a1d1052aa0d",
//         "ingredients": [
//             "great northern bean",
//             "chicken bouillon cubes",
//             "dark brown sugar",
//             "molasses",
//             "cornstarch",
//             "onion",
//             "garlic powder",
//             "mustard powder",
//             "chili powder",
//             "salt",
//             "black pepper",
//             "bacon",
//             "water"
//         ],
//         "minutes": 2970,
//         "n_ingredients": "13",
//         "n_steps": "9",
//         "name": "better then bush s  baked beans",
//         "nutrition": [
//             462.4,
//             28.0,
//             214.0,
//             69.0,
//             14.0,
//             29.0,
//             23.0
//         ],
//         "steps": [
//             "in a very large sauce pan cover the beans and bouillon cubes in 3 inches of water",
//             "bring to a boil , cover , and let sit for 1 1 / 2 hours",
//             "preheat oven to 350 degrees f",
//             "drain and pour beans into a 9'x11' pan",
//             "add the rest over the ingredients , stir , and bake until all the water has evaporated , about 3 hours",
//             "remove from oven , cover , and let sit overnight",
//             "preheat oven to 350 degrees f",
//             "add the next 5 cups of water , and bake until all the water has evaporated , about 3 hours",
//             "serving suggestions: challah bread , steak , hamburgers"
//         ],
//         "submitted": "2003-07-26",
//         "tags": [
//             "weeknight",
//             "time-to-make",
//             "course",
//             "main-ingredient",
//             "cuisine",
//             "preparation",
//             "occasion",
//             "north-american",
//             "side-dishes",
//             "beans",
//             "american",
//             "1-day-or-more",
//             "oven",
//             "potluck",
//             "to-go",
//             "equipment"
//         ]
//     },
//     {
//       "algorithm": "collaborative_item_based",
//       "description": "i'd have to say that this is a labor of love dish, but i give you my word that this recipe is better than bush's. enjoy! oh, and also this recipe is easily doubled. in fact, i think it turns out better when it is.",
//       "id": "64f5b522b5997a1d1052aa0d",
//       "ingredients": [
//           "great northern bean",
//           "chicken bouillon cubes",
//           "dark brown sugar",
//           "molasses",
//           "cornstarch",
//           "onion",
//           "garlic powder",
//           "mustard powder",
//           "chili powder",
//           "salt",
//           "black pepper",
//           "bacon",
//           "water"
//       ],
//       "minutes": 2970,
//       "n_ingredients": "13",
//       "n_steps": "9",
//       "name": "better then bush s  baked beans",
//       "nutrition": [
//           462.4,
//           28.0,
//           214.0,
//           69.0,
//           14.0,
//           29.0,
//           23.0
//       ],
//       "steps": [
//           "in a very large sauce pan cover the beans and bouillon cubes in 3 inches of water",
//           "bring to a boil , cover , and let sit for 1 1 / 2 hours",
//           "preheat oven to 350 degrees f",
//           "drain and pour beans into a 9'x11' pan",
//           "add the rest over the ingredients , stir , and bake until all the water has evaporated , about 3 hours",
//           "remove from oven , cover , and let sit overnight",
//           "preheat oven to 350 degrees f",
//           "add the next 5 cups of water , and bake until all the water has evaporated , about 3 hours",
//           "serving suggestions: challah bread , steak , hamburgers"
//       ],
//       "submitted": "2003-07-26",
//       "tags": [
//           "weeknight",
//           "time-to-make",
//           "course",
//           "main-ingredient",
//           "cuisine",
//           "preparation",
//           "occasion",
//           "north-american",
//           "side-dishes",
//           "beans",
//           "american",
//           "1-day-or-more",
//           "oven",
//           "potluck",
//           "to-go",
//           "equipment"
//       ]
//   },
//   {
//     "algorithm": "collaborative_item_based",
//     "description": "i'd have to say that this is a labor of love dish, but i give you my word that this recipe is better than bush's. enjoy! oh, and also this recipe is easily doubled. in fact, i think it turns out better when it is.",
//     "id": "64f5b522b5997a1d1052aa0d",
//     "ingredients": [
//         "great northern bean",
//         "chicken bouillon cubes",
//         "dark brown sugar",
//         "molasses",
//         "cornstarch",
//         "onion",
//         "garlic powder",
//         "mustard powder",
//         "chili powder",
//         "salt",
//         "black pepper",
//         "bacon",
//         "water"
//     ],
//     "minutes": 2970,
//     "n_ingredients": "13",
//     "n_steps": "9",
//     "name": "better then bush s  baked beans",
//     "nutrition": [
//         462.4,
//         28.0,
//         214.0,
//         69.0,
//         14.0,
//         29.0,
//         23.0
//     ],
//     "steps": [
//         "in a very large sauce pan cover the beans and bouillon cubes in 3 inches of water",
//         "bring to a boil , cover , and let sit for 1 1 / 2 hours",
//         "preheat oven to 350 degrees f",
//         "drain and pour beans into a 9'x11' pan",
//         "add the rest over the ingredients , stir , and bake until all the water has evaporated , about 3 hours",
//         "remove from oven , cover , and let sit overnight",
//         "preheat oven to 350 degrees f",
//         "add the next 5 cups of water , and bake until all the water has evaporated , about 3 hours",
//         "serving suggestions: challah bread , steak , hamburgers"
//     ],
//     "submitted": "2003-07-26",
//     "tags": [
//         "weeknight",
//         "time-to-make",
//         "course",
//         "main-ingredient",
//         "cuisine",
//         "preparation",
//         "occasion",
//         "north-american",
//         "side-dishes",
//         "beans",
//         "american",
//         "1-day-or-more",
//         "oven",
//         "potluck",
//         "to-go",
//         "equipment"
//     ]
// },
// {
//   "algorithm": "collaborative_item_based",
//   "description": "i'd have to say that this is a labor of love dish, but i give you my word that this recipe is better than bush's. enjoy! oh, and also this recipe is easily doubled. in fact, i think it turns out better when it is.",
//   "id": "64f5b522b5997a1d1052aa0d",
//   "ingredients": [
//       "great northern bean",
//       "chicken bouillon cubes",
//       "dark brown sugar",
//       "molasses",
//       "cornstarch",
//       "onion",
//       "garlic powder",
//       "mustard powder",
//       "chili powder",
//       "salt",
//       "black pepper",
//       "bacon",
//       "water"
//   ],
//   "minutes": 2970,
//   "n_ingredients": "13",
//   "n_steps": "9",
//   "name": "better then bush s  baked beans",
//   "nutrition": [
//       462.4,
//       28.0,
//       214.0,
//       69.0,
//       14.0,
//       29.0,
//       23.0
//   ],
//   "steps": [
//       "in a very large sauce pan cover the beans and bouillon cubes in 3 inches of water",
//       "bring to a boil , cover , and let sit for 1 1 / 2 hours",
//       "preheat oven to 350 degrees f",
//       "drain and pour beans into a 9'x11' pan",
//       "add the rest over the ingredients , stir , and bake until all the water has evaporated , about 3 hours",
//       "remove from oven , cover , and let sit overnight",
//       "preheat oven to 350 degrees f",
//       "add the next 5 cups of water , and bake until all the water has evaporated , about 3 hours",
//       "serving suggestions: challah bread , steak , hamburgers"
//   ],
//   "submitted": "2003-07-26",
//   "tags": [
//       "weeknight",
//       "time-to-make",
//       "course",
//       "main-ingredient",
//       "cuisine",
//       "preparation",
//       "occasion",
//       "north-american",
//       "side-dishes",
//       "beans",
//       "american",
//       "1-day-or-more",
//       "oven",
//       "potluck",
//       "to-go",
//       "equipment"
//   ]
// },
// {
//   "algorithm": "collaborative_item_based",
//   "description": "i'd have to say that this is a labor of love dish, but i give you my word that this recipe is better than bush's. enjoy! oh, and also this recipe is easily doubled. in fact, i think it turns out better when it is.",
//   "id": "64f5b522b5997a1d1052aa0d",
//   "ingredients": [
//       "great northern bean",
//       "chicken bouillon cubes",
//       "dark brown sugar",
//       "molasses",
//       "cornstarch",
//       "onion",
//       "garlic powder",
//       "mustard powder",
//       "chili powder",
//       "salt",
//       "black pepper",
//       "bacon",
//       "water"
//   ],
//   "minutes": 2970,
//   "n_ingredients": "13",
//   "n_steps": "9",
//   "name": "better then bush s  baked beans",
//   "nutrition": [
//       462.4,
//       28.0,
//       214.0,
//       69.0,
//       14.0,
//       29.0,
//       23.0
//   ],
//   "steps": [
//       "in a very large sauce pan cover the beans and bouillon cubes in 3 inches of water",
//       "bring to a boil , cover , and let sit for 1 1 / 2 hours",
//       "preheat oven to 350 degrees f",
//       "drain and pour beans into a 9'x11' pan",
//       "add the rest over the ingredients , stir , and bake until all the water has evaporated , about 3 hours",
//       "remove from oven , cover , and let sit overnight",
//       "preheat oven to 350 degrees f",
//       "add the next 5 cups of water , and bake until all the water has evaporated , about 3 hours",
//       "serving suggestions: challah bread , steak , hamburgers"
//   ],
//   "submitted": "2003-07-26",
//   "tags": [
//       "weeknight",
//       "time-to-make",
//       "course",
//       "main-ingredient",
//       "cuisine",
//       "preparation",
//       "occasion",
//       "north-american",
//       "side-dishes",
//       "beans",
//       "american",
//       "1-day-or-more",
//       "oven",
//       "potluck",
//       "to-go",
//       "equipment"
//   ]
// },
// {
//   "algorithm": "collaborative_item_based",
//   "description": "i'd have to say that this is a labor of love dish, but i give you my word that this recipe is better than bush's. enjoy! oh, and also this recipe is easily doubled. in fact, i think it turns out better when it is.",
//   "id": "64f5b522b5997a1d1052aa0d",
//   "ingredients": [
//       "great northern bean",
//       "chicken bouillon cubes",
//       "dark brown sugar",
//       "molasses",
//       "cornstarch",
//       "onion",
//       "garlic powder",
//       "mustard powder",
//       "chili powder",
//       "salt",
//       "black pepper",
//       "bacon",
//       "water"
//   ],
//   "minutes": 2970,
//   "n_ingredients": "13",
//   "n_steps": "9",
//   "name": "better then bush s  baked beans",
//   "nutrition": [
//       462.4,
//       28.0,
//       214.0,
//       69.0,
//       14.0,
//       29.0,
//       23.0
//   ],
//   "steps": [
//       "in a very large sauce pan cover the beans and bouillon cubes in 3 inches of water",
//       "bring to a boil , cover , and let sit for 1 1 / 2 hours",
//       "preheat oven to 350 degrees f",
//       "drain and pour beans into a 9'x11' pan",
//       "add the rest over the ingredients , stir , and bake until all the water has evaporated , about 3 hours",
//       "remove from oven , cover , and let sit overnight",
//       "preheat oven to 350 degrees f",
//       "add the next 5 cups of water , and bake until all the water has evaporated , about 3 hours",
//       "serving suggestions: challah bread , steak , hamburgers"
//   ],
//   "submitted": "2003-07-26",
//   "tags": [
//       "weeknight",
//       "time-to-make",
//       "course",
//       "main-ingredient",
//       "cuisine",
//       "preparation",
//       "occasion",
//       "north-american",
//       "side-dishes",
//       "beans",
//       "american",
//       "1-day-or-more",
//       "oven",
//       "potluck",
//       "to-go",
//       "equipment"
//   ]
// },
// {
//   "algorithm": "collaborative_item_based",
//   "description": "i'd have to say that this is a labor of love dish, but i give you my word that this recipe is better than bush's. enjoy! oh, and also this recipe is easily doubled. in fact, i think it turns out better when it is.",
//   "id": "64f5b522b5997a1d1052aa0d",
//   "ingredients": [
//       "great northern bean",
//       "chicken bouillon cubes",
//       "dark brown sugar",
//       "molasses",
//       "cornstarch",
//       "onion",
//       "garlic powder",
//       "mustard powder",
//       "chili powder",
//       "salt",
//       "black pepper",
//       "bacon",
//       "water"
//   ],
//   "minutes": 2970,
//   "n_ingredients": "13",
//   "n_steps": "9",
//   "name": "better then bush s  baked beans",
//   "nutrition": [
//       462.4,
//       28.0,
//       214.0,
//       69.0,
//       14.0,
//       29.0,
//       23.0
//   ],
//   "steps": [
//       "in a very large sauce pan cover the beans and bouillon cubes in 3 inches of water",
//       "bring to a boil , cover , and let sit for 1 1 / 2 hours",
//       "preheat oven to 350 degrees f",
//       "drain and pour beans into a 9'x11' pan",
//       "add the rest over the ingredients , stir , and bake until all the water has evaporated , about 3 hours",
//       "remove from oven , cover , and let sit overnight",
//       "preheat oven to 350 degrees f",
//       "add the next 5 cups of water , and bake until all the water has evaporated , about 3 hours",
//       "serving suggestions: challah bread , steak , hamburgers"
//   ],
//   "submitted": "2003-07-26",
//   "tags": [
//       "weeknight",
//       "time-to-make",
//       "course",
//       "main-ingredient",
//       "cuisine",
//       "preparation",
//       "occasion",
//       "north-american",
//       "side-dishes",
//       "beans",
//       "american",
//       "1-day-or-more",
//       "oven",
//       "potluck",
//       "to-go",
//       "equipment"
//   ]
// },
// {
//   "algorithm": "collaborative_item_based",
//   "description": "i'd have to say that this is a labor of love dish, but i give you my word that this recipe is better than bush's. enjoy! oh, and also this recipe is easily doubled. in fact, i think it turns out better when it is.",
//   "id": "64f5b522b5997a1d1052aa0d",
//   "ingredients": [
//       "great northern bean",
//       "chicken bouillon cubes",
//       "dark brown sugar",
//       "molasses",
//       "cornstarch",
//       "onion",
//       "garlic powder",
//       "mustard powder",
//       "chili powder",
//       "salt",
//       "black pepper",
//       "bacon",
//       "water"
//   ],
//   "minutes": 2970,
//   "n_ingredients": "13",
//   "n_steps": "9",
//   "name": "better then bush s  baked beans",
//   "nutrition": [
//       462.4,
//       28.0,
//       214.0,
//       69.0,
//       14.0,
//       29.0,
//       23.0
//   ],
//   "steps": [
//       "in a very large sauce pan cover the beans and bouillon cubes in 3 inches of water",
//       "bring to a boil , cover , and let sit for 1 1 / 2 hours",
//       "preheat oven to 350 degrees f",
//       "drain and pour beans into a 9'x11' pan",
//       "add the rest over the ingredients , stir , and bake until all the water has evaporated , about 3 hours",
//       "remove from oven , cover , and let sit overnight",
//       "preheat oven to 350 degrees f",
//       "add the next 5 cups of water , and bake until all the water has evaporated , about 3 hours",
//       "serving suggestions: challah bread , steak , hamburgers"
//   ],
//   "submitted": "2003-07-26",
//   "tags": [
//       "weeknight",
//       "time-to-make",
//       "course",
//       "main-ingredient",
//       "cuisine",
//       "preparation",
//       "occasion",
//       "north-american",
//       "side-dishes",
//       "beans",
//       "american",
//       "1-day-or-more",
//       "oven",
//       "potluck",
//       "to-go",
//       "equipment"
//   ]
// },
// {
//   "algorithm": "collaborative_item_based",
//   "description": "i'd have to say that this is a labor of love dish, but i give you my word that this recipe is better than bush's. enjoy! oh, and also this recipe is easily doubled. in fact, i think it turns out better when it is.",
//   "id": "64f5b522b5997a1d1052aa0d",
//   "ingredients": [
//       "great northern bean",
//       "chicken bouillon cubes",
//       "dark brown sugar",
//       "molasses",
//       "cornstarch",
//       "onion",
//       "garlic powder",
//       "mustard powder",
//       "chili powder",
//       "salt",
//       "black pepper",
//       "bacon",
//       "water"
//   ],
//   "minutes": 2970,
//   "n_ingredients": "13",
//   "n_steps": "9",
//   "name": "better then bush s  baked beans",
//   "nutrition": [
//       462.4,
//       28.0,
//       214.0,
//       69.0,
//       14.0,
//       29.0,
//       23.0
//   ],
//   "steps": [
//       "in a very large sauce pan cover the beans and bouillon cubes in 3 inches of water",
//       "bring to a boil , cover , and let sit for 1 1 / 2 hours",
//       "preheat oven to 350 degrees f",
//       "drain and pour beans into a 9'x11' pan",
//       "add the rest over the ingredients , stir , and bake until all the water has evaporated , about 3 hours",
//       "remove from oven , cover , and let sit overnight",
//       "preheat oven to 350 degrees f",
//       "add the next 5 cups of water , and bake until all the water has evaporated , about 3 hours",
//       "serving suggestions: challah bread , steak , hamburgers"
//   ],
//   "submitted": "2003-07-26",
//   "tags": [
//       "weeknight",
//       "time-to-make",
//       "course",
//       "main-ingredient",
//       "cuisine",
//       "preparation",
//       "occasion",
//       "north-american",
//       "side-dishes",
//       "beans",
//       "american",
//       "1-day-or-more",
//       "oven",
//       "potluck",
//       "to-go",
//       "equipment"
//   ]
// },
// {
//   "algorithm": "collaborative_item_based",
//   "description": "i'd have to say that this is a labor of love dish, but i give you my word that this recipe is better than bush's. enjoy! oh, and also this recipe is easily doubled. in fact, i think it turns out better when it is.",
//   "id": "64f5b522b5997a1d1052aa0d",
//   "ingredients": [
//       "great northern bean",
//       "chicken bouillon cubes",
//       "dark brown sugar",
//       "molasses",
//       "cornstarch",
//       "onion",
//       "garlic powder",
//       "mustard powder",
//       "chili powder",
//       "salt",
//       "black pepper",
//       "bacon",
//       "water"
//   ],
//   "minutes": 2970,
//   "n_ingredients": "13",
//   "n_steps": "9",
//   "name": "better then bush s  baked beans",
//   "nutrition": [
//       462.4,
//       28.0,
//       214.0,
//       69.0,
//       14.0,
//       29.0,
//       23.0
//   ],
//   "steps": [
//       "in a very large sauce pan cover the beans and bouillon cubes in 3 inches of water",
//       "bring to a boil , cover , and let sit for 1 1 / 2 hours",
//       "preheat oven to 350 degrees f",
//       "drain and pour beans into a 9'x11' pan",
//       "add the rest over the ingredients , stir , and bake until all the water has evaporated , about 3 hours",
//       "remove from oven , cover , and let sit overnight",
//       "preheat oven to 350 degrees f",
//       "add the next 5 cups of water , and bake until all the water has evaporated , about 3 hours",
//       "serving suggestions: challah bread , steak , hamburgers"
//   ],
//   "submitted": "2003-07-26",
//   "tags": [
//       "weeknight",
//       "time-to-make",
//       "course",
//       "main-ingredient",
//       "cuisine",
//       "preparation",
//       "occasion",
//       "north-american",
//       "side-dishes",
//       "beans",
//       "american",
//       "1-day-or-more",
//       "oven",
//       "potluck",
//       "to-go",
//       "equipment"
//   ]
// }
// ]

  constructor(private route: ActivatedRoute, private recipesService: RecipesService, private location: Location, public router: Router) { }

  ngOnInit(): void {
    this.route.queryParamMap.subscribe(params => {
      const data = params.get('recipe');
      if(data){
        this.recipe = JSON.parse(decodeURIComponent(data));
        this.fetchRecipes(this.recipe);
      }
    })
  }


  navigateBack(): void {
    this.router.navigate(['/recipesLists']);
  }

  fetchRecipes(recipe: any){
    this.recipesService.recommend_content_based_by_recipeID(15, recipe.id, "64f5d5f084de34f5c115788b", []).subscribe((data) => {
      if(data){
        this.showSpinner = false;
        this.recipesList = data;
        this.recipesService.increment_user_recipe_views(this.user_id, recipe.id).subscribe((data) => {
          console.log(data);
        });
      }
    });
  }


}