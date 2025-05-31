import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel

# Chargement du modèle une seule fois
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# Liste de concepts à tester (à améliorer plus tard)
CANDIDATES = [
    # Pose & Style
    "nude woman", "nude man", "topless", "bottomless", "lingerie", "bikini", "underwear",
    "transparent clothes", "wet shirt", "provocative pose", "posing nude", "pin-up",
    "softcore", "hardcore", "solo pose", "mirror selfie", "close-up", "body shot",
    "full body", "crotch shot", "cleavage", "cameltoe",

    # Anatomie
    "bare breasts", "small breasts", "big breasts", "areola", "nipples", "bare butt",
    "buttocks", "spread legs", "genitals", "vagina", "penis", "erection", "pubic hair",
    "shaved pussy", "hairy pussy", "cumshot", "anal", "wet", "aroused", "orgasm",

    # Action sexuelle
    "sex scene", "blowjob", "doggy style", "missionary", "cowgirl", "reverse cowgirl",
    "fingering", "masturbation", "lesbian sex", "gay sex", "bisexual threesome",
    "group sex", "69", "anal sex", "oral sex", "double penetration", "cum inside",
    "cum on face", "creampie", "spanking", "threesome",

    # Genres visuels
    "realistic photo", "3d render", "anime style", "hentai", "manga", "ecchi",
    "AI generated", "painting", "sketch", "pixel art", "digital art", "illustration",

    # Fétiches & Cosplay
    "BDSM", "dominatrix", "latex suit", "bondage", "rope play", "gagged", "choker",
    "schoolgirl uniform", "maid outfit", "nurse outfit", "milf", "teen girl",
    "mature woman", "yuri", "yaoi", "tentacle", "sex toy", "vibrator",
    "dildo", "panties",

    # Visuels & ambiance
    "red lipstick", "high heels", "wet skin", "tan lines", "tattoo", "pierced nipple",
    "g-string", "stockings", "fishnet", "heels", "cum", "sweaty", "bedroom",
    "shower scene", "bath scene", "mirror", "lingerie model", "suggestive eyes",
    "touching body", "biting lips"
    
    "nurse", "schoolgirl", "teacher", "secretary", "maid", "waitress",
    "policewoman", "businesswoman", "cheerleader", "flight attendant", "military uniform",
    "firefighter", "doctor", "receptionist", "lawyer"
    
    "latex", "leather outfit", "fishnet stockings", "tight dress", "high heels",
    "short skirt", "cleavage", "corset", "pantyhose", "see-through fabric",
    "off-shoulder top", "crop top", "yoga pants", "bodysuit", "backless dress"
    
    "nun", "anime girl", "catgirl", "bunny girl", "elf", "goth girl",
    "demon girl", "succubus", "angel", "fairy", "cosplay", "idol",
    "gyaru", "e-girl", "streamer", "influencer"
    
    "suggestive look", "biting lips", "flirting", "posing seductively",
    "touching lips", "arched back", "looking over shoulder", "winking",
    "stretching", "kneeling", "on all fours", "licking finger", "pouting"
]

def generate_tags(image_path, top_k=5):
    """
    Génère des tags NSFW intelligents pour une image donnée.
    """
    try:
        image = Image.open(image_path).convert("RGB")
    except Exception as e:
        print(f"[CLIP] Erreur de chargement image : {e}")
        return []

    inputs = processor(text=CANDIDATES, images=image, return_tensors="pt", padding=True)
    outputs = model(**inputs)

    logits_per_image = outputs.logits_per_image  # shape: [1, len(CANDIDATES)]
    probs = logits_per_image.softmax(dim=1).squeeze()

    top_indices = probs.topk(top_k).indices.tolist()
    tags = [CANDIDATES[i] for i in top_indices]

    return tags

def get_clip_embedding(image_path):
    image = Image.open(image_path).convert("RGB")
    inputs = processor(images=image, return_tensors="pt")
    with torch.no_grad():
        image_features = model.get_image_features(**inputs)
    image_features /= image_features.norm(p=2, dim=-1)  # normalisation
    return image_features.squeeze().tolist()  # vecteur 512D