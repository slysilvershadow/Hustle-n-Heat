import random

GENES = {
    "main": {
        "sex": ["x", "y"],
        "skin tone": ["pale", "medium", "tan", "dark", "deep"],
        "skin undertone": ["warm", "neutral", "cool"],
        "height": ["short", "average", "tall"],
        "bodyshape": ["slim", "average", "athletic", "curvy"],
        "bodysize": ["small", "medium", "large"],
        "eyecolor": ["brown", "hazel", "green", "blue", "grey"],
        "external coverings": ["hair", "scales", "hide", "feathers", "shell", "exoskeleton"]
    },
    "BodyParts": {
        "Limbs": {
            "Arms": ["Flipper-like", "Human", "Streamlined", "Strong and muscled", "Slender", "Slimy and agile", "Flexible"],
            "Legs": ["Paddle-like", "Human", "Webbed", "Sturdy", "Long and agile", "Powerful for leaping", "Gripping"]
        },
        "Special Appendages": {
            "Lower": {
                "Tails": ["Fish-like", "Thin and elongated", "Short and thick", "Long and slender", "Prehensile", "Grasping"]
            },
            "Upper": {
                "Wings": ["Short and strong", "Wide and soaring", "Large and powerful", "Fast and narrow", "Broad and silent", "Agile and maneuverable"],
                "Fins": ["Large and strong", "Streamlined", "Stubby and resilient", "Thin and long", "Broad and flexible", "Small and decorative"]
            }
        },
        "Claws": ["Flat and wide", "Curved", "Hooked", "Sharp and retractable", "Webbed and pointed", "Grasping"],
        "Horns": ["Smooth and curved", "Small and ridged", "Large and spiraled", "Long and straight", "Twisted", "Branched"],
        "Ears": ["Small and streamlined", "Rounded", "Furry and pointed", "Large and keen", "Tufted", "Flexible and rotating"],
        "Eyes": ["Round and large", "Almond-shaped", "Sharp and focused", "Wide and scanning", "Upturned", "Hooded"],
        "Noses": ["Blowhole", "Small Human (Refined)", "Soft Human (Perky)", "Medium Human (Dainty)", "Strong Human (Hero)", "Tall Human (Bulb)", "Sensitive Human (Soft)", "Medium Human (Strong)", "Flexible Human (Upturned)", "Small Human (Perky)", "Bear", "Almond Human (Refined)"],
        "Mouths": ["Beaked", "Wide and gaping", "Thin-lipped", "Small and sharp", "Strong-jawed", "Gripping", "Fanged", "Slender", "Flexible and extending", "Amphibious", "Hooked", "Small and sharp"]
    }
}

class Gene:
    """Represents a gene with a binary representation."""
    def __init__(self, name, possibilities):
        self.name = name
        self.possibilities = possibilities
        self.binary_representations = self.generate_binary_representations()

    def generate_binary_representations(self):
        binary_representations = {}
        for i, possibility in enumerate(self.possibilities):
            binary_representation = bin(i)[2:].zfill(len(self.possibilities).bit_length())
            binary_representations[possibility] = binary_representation
        return binary_representations

    def get_binary_representation(self, possibility):
        return self.binary_representations.get(possibility)

    def __str__(self):
        return f"{self.name}: {self.possibilities}"

class Character:
    """Represents a character with two sets of genes."""
    def __init__(self, main_genes, body_parts_genes):
        self.main_genes = main_genes
        self.body_parts_genes = body_parts_genes

    def generate_sprite(self):
        """Generates a sprite representation based on the character's genes."""
        sprite = {}
        
        # Add main genes to sprite
        for gene_name, gene_value in self.main_genes.items():
            sprite[gene_name] = gene_value
        
        # Handle body parts with conditional replacements
        arms = self.body_parts_genes.get("Arms")
        legs = self.body_parts_genes.get("Legs")
        wings = self.body_parts_genes.get("Wings")
        fins = self.body_parts_genes.get("Fins")
        tail = self.body_parts_genes.get("Tails")

        # Replace arms with wings or fins if applicable
        if wings or fins:
            sprite["Arms"] = "Replaced by " + (wings if wings else fins)
        else:
            sprite["Arms"] = arms

        # Replace legs with tail if applicable
        if tail:
            sprite["Legs"] = "Replaced by Tail: " + tail
        else:
            sprite["Legs"] = legs

        # Add other body parts
        for part_name, part_value in self.body_parts_genes.items():
            if part_name not in ["Arms", "Legs"]:  # Already handled above
                sprite[part_name] = part_value

        return sprite

    def __str__(self):
        return f"Character with genes: {self.main_genes}, Body Parts: {self.body_parts_genes}"

def create_random_character():
    """Creates a random character with random genes."""
    main_genes = {gene_name: random.choice(possibilities) for gene_name, possibilities in GENES["main"].items()}
    body_parts_genes = {part_name: random.choice(possibilities) for part_name, possibilities in flatten_body_parts(GENES["BodyParts"]).items()}
    return Character(main_genes, body_parts_genes)

def flatten_body_parts(body_parts):
    """Flattens the body parts dictionary for easier random selection."""
    flattened = {}
    for category, parts in body_parts.items():
        if isinstance(parts, dict):  # Check if parts is a dictionary
            for part_name, possibilities in parts.items():
                if isinstance(possibilities, list):  # If it's a list, add it directly
                    flattened[part_name] = possibilities
                elif isinstance(possibilities, dict):  # If it's a nested dictionary, go deeper
                    for sub_part_name, sub_possibilities in possibilities.items():
                        flattened[sub_part_name] = sub_possibilities
        elif isinstance(parts, list):  # If the category itself is a list
            flattened[category] = parts  # Add the list directly
    return flattened

# Example usage
if __name__ == "__main__":
    character = create_random_character()
    print(character)
    sprite = character.generate_sprite()
    print("Sprite representation:", sprite)


import random
from entities.life.genes import GENES 

class GeneInstance:
    def __init__(self, name, value):
        self.name = name
        self.value = value

class DNA:
    """
    Represents the DNA of an entity, containing traits inherited from parents.
    """

    def __init__(self, mother_dna=None, father_dna=None):
        self.genes = {}
        if mother_dna and father_dna:
            self.inherit_traits(mother_dna, father_dna)
        else:
            self.generate_random_traits()

    def create_gene(self, name, options):
        return GeneInstance(name, random.choice(options))

    def is_valid_trait(self, gene):
        return gene.name in GENES["main"] or gene.name in GENES["BodyParts"]

    def express_traits(self):
        return {gene.name: gene.value for gene in self.genes.values()}

    def inherit_traits(self, mother_dna, father_dna):
        for category, traits in GENES.items():
            for trait, options in traits.items():
                mother_trait = mother_dna.genes[trait].value
                father_trait = father_dna.genes[trait].value
                self.genes[trait] = self.create_gene(trait, [mother_trait, father_trait])

    def generate_random_traits(self):
        for category, traits in GENES.items():
            for trait, options in traits.items():
                print(f"Generating trait: {trait}, Options: {options}")  # Debugging line
                if isinstance(options, dict):  # Check if options is a dictionary
                    # If options is a dictionary, iterate through its items
                    for sub_trait, sub_options in options.items():
                        if isinstance(sub_options, list):  # Check if sub_options is a list
                            self.genes[sub_trait] = self.create_gene(sub_trait, sub_options)
                        elif isinstance(sub_options, dict):  # If it's a nested dictionary
                            for nested_trait, nested_options in sub_options.items():
                                self.genes[nested_trait] = self.create_gene(nested_trait, nested_options)
                else:
                    # If options is a list, create gene normally
                    self.genes[trait] = self.create_gene(trait, options)

# Example usage
mother_dna = DNA()
father_dna = DNA()
child_dna = DNA(mother_dna, father_dna)
print(child_dna.express_traits())


import random
from entities.life.dna import DNA
from entities.life.genes import GENES
from entities.survival.needs import Needs  # Import the Needs class
from entities.characters.stats import Stat  # Adjust this if stats is in the same directory
from actions.action import ActionQueue, Action, Command  # Adjust if actions is in a different directory

class Character:
    def __init__(self, is_player=False, dna=None, x=None, y=None, age=None, father=None, mother=None, family=None, name=None):
        self.is_player = is_player
        self.dna = dna if dna else DNA()  # Use DNA class to initialize DNA
        self.x = x
        self.y = y
        self.age = age
        self.father = father
        self.mother = mother
        self.family = family
        self.name = name if name else self.generate_name()
        self.stats = {
            'core': {
                'stamina': Stat('Stamina', 1),
                'strength': Stat('Strength', 1),
                'dexterity': Stat('Dexterity', 1),
                'perception': Stat('Perception', 1),
                'willpower': Stat('Willpower', 1)
            },
            'advanced': {}
        }
        self.skills = self.initialize_skills()  # Initialize skills
        self.traits = self.initialize_traits()  # Initialize traits
        self.needs = Needs()  # Initialize needs using the Needs class
        self.action_queue = ActionQueue()  # Initialize action queue

        # Calculate advanced stats based on the initial core stats
        self.update_advanced_stats()
        self.update_needs()

        # Handle family relationships
        if family:
            family.add_member(self)
        else:
            self.family = self.create_new_family()

        # Handle last name generation based on father
        if father:
            last_name = father.name.split()[-1]
        else:
            last_name = self.generate_last_name()

        self.name = f"{self.name} {last_name}"

    def perform_actions(self):
        """Execute queued commands."""
        self.action_queue.execute_next_action(self)
        self.needs.update_needs()  # Update needs after performing actions

    def initialize_traits(self):
        """Initialize traits for the character based on predefined categories."""
        return self.dna.express_traits()  # Use DNA to express traits

    def generate_name(self):
        """Generate a random or default first name."""
        return "Unnamed"  # Replace this with actual name generation logic if needed

    def generate_last_name(self):
        """Generate a random or default last name."""
        return "Smith"  # Replace this with actual last name generation logic if needed

    def create_new_family(self):
        """Create a new family object for the character if none exists."""
        return Family()  # Replace with actual family creation logic

    def generate_offspring(self, parent2_dna):
        """Generate offspring DNA based on parents' DNA."""
        return DNA(self.dna, parent2_dna)

    def create_sprite(self):
        """Create sprite (simplified representation of the traits)."""
        return self.dna.express_traits()

# Example usage
if __name__ == "__main__":
    # Create two parent characters
    mother = Character(name="Alice")
    father = Character(name="Bob")

    # Generate offspring
    child_dna = mother.generate_offspring(father.dna)
    child = Character(dna=child_dna, name="Charlie")

    # Print traits of the child
    print(f"Child's traits: {child.create_sprite()}")

