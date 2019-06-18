class Unit:
    """Tools for units converting and calculation
    """

    @staticmethod
    def c2f(celsius):
        """Convert Celsius to Fahrenheit
        
        Arguments:
            celsius {float} -- [degree, unit is celsius]

        Returns:
            [float] -- [degree, unit is fahrenheit]
        """
        return round((celsius * 1.8 + 32), 2)
    
    
    @staticmethod
    def sg2plato(sg):
        """Convert Specific Gravity to Plato
        
        Arguments:
            sg {float} -- [specific gravity, eg. measured by hydrometer]
        
        Returns:
            [float] -- [Plato, unit is degree P]
        """

        plato = (-1 * 616.868) + (1111.14 * sg) - (630.272 * sg**2) + (135.997 * sg**3)
        return round(plato, 1)

    @staticmethod
    def plato2sg(plato):
        """Convert Plato to Specific Gravity
        
        Arguments:
            plato {float} -- [Plato, unit is degree P]
        
        Returns:
            [float] -- [specific gravity, eg. 1.012]
        """

        sg = 1 + (plato / (258.6 - ((plato / 258.2) * 227.1)))
        return round(sg, 3)

    @staticmethod
    def calc_abv(og, fg):
        """Calculate Alcohol By Volume with Orginial Gravity & Final Gravity
        
        Arguments:
            og {float} -- [Orinigal Gravity, eg. 1.080]
            fg {float} -- [Final Gravity, eg. 1.021]
        
        Returns:
            [float] -- [Alcohol By Volume in percentage, eg. 5.65%]
        """

        abv = (og - fg) * 131.52
        return round(abv, 2)