def guess_category(tags):
    from collections import defaultdict
    CATEGORY_RULES = {
    "Cosplay": [
        "maid", "nun", "bunny", "schoolgirl", "teacher", "nurse", "kigurumi",
        "armor", "costume", "uniform"
    ],
    "Amateur": [
        "mirror", "selfie", "bathroom", "bedroom", "realistic", "phone", "snapchat"
    ],
    "Anime": [
        "anime", "manga", "2d", "hentai", "drawn", "doujin", "waifu", "ecchi"
    ],
    "Fetish": [
        "latex", "leather", "feet", "bondage", "gag", "rope", "heels", "collar", "whip", "chains"
    ],
    "NSFW-Soft": [
        "lingerie", "cleavage", "panties", "underwear", "thighs", "bikini", "see-through", "nipple-slip"
    ],
    "NSFW-Hard": [
        "nude", "penetration", "sex", "cum", "oral", "anal", "group", "69", "fingering", "orgasm"
    ],
    "Solo": [
        "solo", "masturbation", "toys", "fingering", "mirror selfie"
    ],
    "Couple": [
        "kiss", "couple", "duo", "intercourse", "partner", "hug"
    ],
    "Furry / Monster": [
        "furry", "tentacle", "monster", "dragon", "beast", "nekopara", "ears", "tails"
    ],
    "Fantasy": [
        "succubus", "demon", "angel", "horns", "wings", "fairy", "magic", "wizard", "elf", "goblin"
    ],
    "Outdoor / Public": [
        "public", "outdoor", "beach", "forest", "car", "park", "balcony"
    ],
    "SFW": [
        "smile", "portrait", "face", "aesthetic", "outfit", "fashion", "pose"
    ],
}

    tag_set = set(tag.lower() for tag in tags)
    match_scores = defaultdict(int)

    for category, keywords in CATEGORY_RULES.items():
        for keyword in keywords:
            if keyword in tag_set:
                match_scores[category] += 1

    if match_scores:
        return max(match_scores, key=match_scores.get)

    return "Autre"
