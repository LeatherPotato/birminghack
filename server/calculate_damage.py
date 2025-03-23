import pronouncing
from sentence_transformers import SentenceTransformer, util

# Testing with values
oppStrength = "slaying" # Opponent's strength
oppWeakness = "tea"     # Opponent's weakness
opponent_defence = 0.25 # 25% damage reduction
player_lethality = 15   # Base damage of the player

rap_lines = [
    "That check dropping, paying",
    "Cause they fall, yeah, they get slain",
    "It's scalding hot like tea",
    "But honestly with it you can't even see"
]

# The model to calculate the similarity score
model = SentenceTransformer('sentence-transformers/nli-mpnet-base-v2')

# Functions

# Get similarity between sentences/phrases/words
def get_similarity(sentence1, sentence2):
    # Calculate cosine similarity between two sentences
    # We also normalize it to [0,1] (positive) as it can become negative
    emb1 = model.encode(sentence1, convert_to_tensor=True)
    emb2 = model.encode(sentence2, convert_to_tensor=True)
    raw_score = util.pytorch_cos_sim(emb1, emb2).item()
    # Normalize the score from [-1, 1] to [0, 1]
    return (raw_score + 1) / 2

# This function extracts the last word from a line
def get_last_word(line):
    # Keep track of all punctuation to remove
    punctuation = ".,;:!?\"'()-"
    # Get all the words from the line, normalise them to lowercase and split them
    words = line.strip().lower().split()
    # Get rid of all the spaces
    if not words:
        return ""
    # The last word
    last = words[-1]
    # Remove any leading/trailing punctuation
    return last.strip(punctuation)

# Check the rhyme for each line by comparing the last words of each line
def check_rhyme(line1, line2):
    # Returns True if the last word of line1 rhymes with the last word of line2
    last_word1 = get_last_word(line1)
    last_word2 = get_last_word(line2)
    return last_word2 in pronouncing.rhymes(last_word1)

# Counts total syllables in a line
def count_syllables(line):
    # Keep track of punctuation to remove
    punctuation = ".,;:!?\"'()-"
    words = line.strip().lower().split()
    total = 0
    # For each word strip away the punctuation and then look for the num of syllables in each word
    for word in words:
        word_clean = word.strip(punctuation)
        phones = pronouncing.phones_for_word(word_clean)
        # If there are actual words and the syllables exist
        if phones:
            # Keep track of the no of syllables in total and increment
            total += pronouncing.syllable_count(phones[0])
    return total

# Checks for the same syllable count in each line
def check_same_syllable_count(line1, line2):
    # Returns True if both lines have the same total syllable count
    return count_syllables(line1) == count_syllables(line2)

# Constant bonus multipliers
DEFAULT_RHYME_BONUS = 1.0
BONUS_RHYME_MULT = 1.2
DEFAULT_SYLLABLE_BONUS = 1.0
BONUS_SYLLABLE_MULT = 1.1

# Damage calculation loop

# This list keeps track of the damage of each line
damage_results = []

# rap_lines in this case is 4
for i in range(len(rap_lines)):
    # Get the first line
    line = rap_lines[i]
    
    # Calculate normalized similarity scores against opponent's strength and weakness
    strength_score = round(get_similarity(line, oppStrength), 2)
    weakness_score = round(get_similarity(line, oppWeakness), 2)
    
    # Calculate similarity ratio using normalized scores (avoid division by zero by checking strength_score)
    if strength_score == 0:
        similarity_ratio = 0
    else:
        similarity_ratio = round(weakness_score / strength_score, 2)
    
    # Initialize bonus multipliers
    rhyme_bonus = DEFAULT_RHYME_BONUS
    syllable_bonus = DEFAULT_SYLLABLE_BONUS

    # Compare the current line with all other lines
    for j in range(len(rap_lines)):
        if i == j:
            continue  # Skip self-comparison
        
        if check_rhyme(line, rap_lines[j]):
            rhyme_bonus = BONUS_RHYME_MULT
        if check_same_syllable_count(line, rap_lines[j]):
            syllable_bonus = BONUS_SYLLABLE_MULT

    # Calculate total multiplier and final damage
    # Round so the damage is in integers only
    total_multiplier = similarity_ratio * rhyme_bonus * syllable_bonus
    damage = round(player_lethality * total_multiplier * (1 - opponent_defence))
    damage_results.append(damage)

    # Testing
    print("Line", i + 1, ":", line)
    print("  Strength Score:", strength_score, ", Weakness Score:", weakness_score)
    print("  Similarity Ratio:", similarity_ratio)
    print("  Rhyme Bonus:", rhyme_bonus, ", Syllable Bonus:", syllable_bonus)
    print("  => Damage:", damage, "\n")

# Find the total sum of damage
total_damage = sum(damage_results)
print("Total Damage Dealt:", total_damage)
