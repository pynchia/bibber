Feature: Homepage
	Scenario: homepage when game is off
		Given the game is off
		When I go to the homepage
		Then the page shows 

	Scenario: homepage when game is on
		Given the game is on
		When I go to the homepage
		Then the page shows 
