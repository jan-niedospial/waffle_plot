# Waffle Plot function

The idea behind building it it was to create a reliable, easy-to-use yet customizable waffle plot that wouldn't require any not-widely-used libraries (it only requires native Python and matplotlib). It is supposed to be resilient enough to be used in most scenarios even in automated processing, much like plots in matplotlib.

As a result the function is slightly over-engineered to account for some unusual scenarios that can easily happen in automated processing.

Please consider checking the examples in Jupyter Notebook file to get a better grasp of how the parameters for the function work in practice.

One thing not covered in the examples is changing the default values for keyword arguments in the function. Please feel free to experiment with them if the current ones don't meet your needs.


# Attributions
The function was based on the brilliant piece of code by Justin Fletcher, posted on Stack Overflow on 03 Jan 2017.

Link: https://stackoverflow.com/questions/41400136/how-to-do-waffle-charts-in-python-square-piechart

Discounting pywaffle and attempted use of squarify (another third-party library), it is the only viable piece of code for a waffle plot I found, copied many times over by different people. Some of them added things to it, but it was mostly the same code. As the author states clearly, this solution is not finished. But it was a very good start.

I used fragments added in the same post in 18 Jun 2019 by Carlos García Rosales, mainly around the value_sign variable.

Some improvements to the function were made by using ChatGPT. Namely removing the numpy library and replacing it with basic python code, removing one intermediate variable, and improving the docstring.

Eduardo H. Salazar Caldentey guided me away from an illegible block of code to something that, at least from a certain distance, looks like an actual OOP.

# A few words about the License

This repo is published under CC-BY-SA 4.0.

I really wanted to publish it under MIT License, but I used some of the code from Stack Overflow. And everything the users publish on Stack Overflow is under CC-BY-SA. More about that here: https://stackoverflow.com/help/licensing. Share-Alike is Share-Alike.

