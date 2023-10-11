import unittest
from app import get_characteristics, extract_character_id, compute_characteristics_score, \
    get_images

class testClass(unittest.TestCase):
    def test_get_characteristics(self):
        #Test with non existing SW character
        response, response_id = get_characteristics("0")
        self.assertEqual(response,None)
        self.assertEqual(response_id,None)

        #Test with valid SW character
        response, response_id = get_characteristics("Luke")
        self.assertEqual(response["Name"],"Luke Skywalker")
        self.assertEqual(response["Gender"],"Male")
        self.assertEqual(response_id, "1")


    def test_extract_character_id(self):
        #Test extraction of character id with single digit
        url = "https://swapi.dev/api/people/1/"
        response_id = extract_character_id(url)
        self.assertEqual(response_id,"1")

        #Test extraction of character id with double digits
        url = "https://swapi.dev/api/people/14/"
        response_id = extract_character_id(url)
        self.assertEqual(response_id,"14")


    def test_compute_characteristics_score(self):
        #Test that scores are tallied correctly and that correct character wins
        characters = [{"Name":"Leia","Height":"65","Films":2},{"Name":"Yoda","Height":"14","Films":7}]
        response, response_winner = compute_characteristics_score(characters)
        self.assertEqual(response[0]["Score"],67)
        self.assertEqual(response[1]["Score"],21)
        self.assertEqual(response_winner,"Leia")


    def test_get_images(self):
        #Test that image urls are generated correctly
        id1 = "14"
        id2 = "2"
        response = get_images(id1, id2)
        self.assertEqual(response[0],"14.jpg")
        self.assertEqual(response[1],"2.jpg")
