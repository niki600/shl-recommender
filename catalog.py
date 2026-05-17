# catalog.py
# Ye file SHL catalog load karti hai aur search karne ka kaam karti hai

import json
import os
import re
from typing import List, Dict


def load_catalog(path: str = "data/catalog.json") -> List[Dict]:
    """JSON file se catalog load karo"""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_test_type(keys: List[str]) -> str:
    """
    Assessment ke 'keys' field se short type code nikalo
    Assignment mein test_type field chahiye response mein
    """
    if not keys:
        return "K"
    
    key = keys[0].lower()
    
    if "personality" in key or "behavior" in key:
        return "P"
    elif "ability" in key or "aptitude" in key:
        return "A"
    elif "simulation" in key:
        return "S"
    elif "competenc" in key:
        return "C"
    elif "biodata" in key or "situational" in key:
        return "B"
    elif "development" in key or "360" in key:
        return "D"
    else:
        return "K"  # Knowledge & Skills default


def search_catalog(
    catalog: List[Dict],
    query: str,
    job_level: str = "",
    max_results: int = 10
) -> List[Dict]:
    """
    Catalog mein keyword search karo
    
    Logic:
    - Query ke words ko description, name aur keys mein dhundho
    - Job level match karo agar diya hai
    - Score ke basis pe sort karo
    - Top max_results return karo
    """
    query_lower = query.lower()
    query_words = re.findall(r'\w+', query_lower)
    
    # Common words ignore karo (stop words)
    stop_words = {
        'a', 'an', 'the', 'is', 'are', 'was', 'were', 'be', 'been',
        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
        'could', 'should', 'may', 'might', 'i', 'we', 'you', 'he',
        'she', 'it', 'they', 'for', 'in', 'on', 'at', 'to', 'of',
        'and', 'or', 'but', 'not', 'with', 'this', 'that', 'test',
        'assessment', 'measures', 'knowledge', 'hiring', 'need',
        'want', 'looking', 'someone', 'who', 'can', 'able', 'also',
        'new', 'our', 'also', 'some', 'any'
    }
    
    meaningful_words = [w for w in query_words if w not in stop_words and len(w) > 2]
    
    results = []
    
    for item in catalog:
        score = 0
        
        name = item.get("name", "").lower()
        description = item.get("description", "").lower()
        keys = [k.lower() for k in item.get("keys", [])]
        keys_text = " ".join(keys)
        item_levels = [l.lower() for l in item.get("job_levels", [])]
        
        # Har meaningful word ke liye score badhao
        for word in meaningful_words:
            if word in name:
                score += 5          # Name mein match = zyada important
            if word in description:
                score += 2          # Description mein match
            if word in keys_text:
                score += 3          # Category match
        
        # Job level bonus
        if job_level:
            jl = job_level.lower()
            for level in item_levels:
                if jl in level or level in jl:
                    score += 4
                    break
            # Common mappings
            if ("mid" in jl or "senior" in jl or "experienced" in jl) and \
               any("mid-professional" in l or "professional" in l for l in item_levels):
                score += 2
            if ("junior" in jl or "entry" in jl or "fresher" in jl) and \
               any("entry" in l or "graduate" in l for l in item_levels):
                score += 2
        
        # Status ok hona chahiye aur remote hona chahiye
        if item.get("status") != "ok":
            continue
        
        if score > 0:
            results.append((score, item))
    
    # Score ke basis pe sort karo (high to low)
    results.sort(key=lambda x: x[0], reverse=True)
    
    # Sirf items return karo, score nahi
    return [item for score, item in results[:max_results]]


def format_for_response(items: List[Dict]) -> List[Dict]:
    """
    Catalog items ko response format mein convert karo
    Returns list of {name, url, test_type}
    """
    formatted = []
    for item in items:
        formatted.append({
            "name": item.get("name", ""),
            "url": item.get("link", ""),
            "test_type": get_test_type(item.get("keys", []))
        })
    return formatted


def get_items_by_name(catalog: List[Dict], names: List[str]) -> List[Dict]:
    """Naam se specific items dhundho (comparison ke liye)"""
    results = []
    for item in catalog:
        item_name = item.get("name", "").lower()
        for name in names:
            if name.lower() in item_name or item_name in name.lower():
                results.append(item)
                break
    return results
