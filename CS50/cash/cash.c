#include <cs50.h>
#include <math.h>
#include <stdio.h>

int main(void)
{
    float input;
    
    do
    {
        input = get_float("Change owed: ");
    }
    while (input < 0);

    int cents;
    if (input >= 100)
    {
        cents = round(input);  
    }
    else
    {
        cents = round(input * 100); 
    }

    int coins = 0;

    // Quarters (25 cents)
    coins += cents / 25;
    cents %= 25;

    // Dimes (10 cents)
    coins += cents / 10;
    cents %= 10;

    // Nickels (5 cents)
    coins += cents / 5;
    cents %= 5;

    // Pennies (1 cent)
    coins += cents;

    printf("%i\n", coins);
}
