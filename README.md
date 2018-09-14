# make_monsters_feel_crappy
A simple single-player, turn-based, numerical strategic survival game for the command line.

![Gameplay](https://raw.githubusercontent.com/marcelgarus/make_monsters_feel_crappy/master/image.png)

Your job is to save the helpless village from an army of monsters marching towards it.

After the introductory line at the top, there is a line that represents the current situation, where each number represents the HP of one monster:

`helpless village _ _ _ 5 3 5 6 6 4 5 7 5`

Every turn, the monsters will march on one field to the left, getting nearer and nearer to the village.
And it gets worse, the monsters get stronger the more of them you kill!

But every turn, you have the chance to do one of three actions to delay the inevitable as far as possible:-

- Shoot the monsters!
  There are several weapons you can choose from:
  - Constant Cannon (`c`):
    A cannon which hurts every monster by the same base level amount of HP.
  - Linear Laser (`l`):
    A laser which hurts the first monster with the base level amount of HP, the second monster double, the third monster triple etc.
  - Gaussian Granade (`g`):
    A granade which hurts the strongest monster by the base level and some monsters around it to a lesser degree.
- Increase the range (`r`):
  - You will see further and be able to hurt more monsters.
- Upgrade your weapons (`u`). Increases the damage base level by one.
