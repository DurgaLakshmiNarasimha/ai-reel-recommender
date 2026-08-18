def analyze_reel(reel):
    """
    Analyze a reel and extract its underlying topic,
    context, and apparent user interest.
    """

    text = " ".join([
        reel.get("title", ""),
        reel.get("caption", ""),
        reel.get("transcript", ""),
        reel.get("visual_description", "")
    ]).lower()

    if any(word in text for word in [
        "java",
        "coding",
        "programmer",
        "software engineer",
        "developer"
    ]):
        main_topic = "Software Engineering"
        subtopics = [
            "Programming",
            "Software Development"
        ]
        context = "Technology and software development"
        apparent_interest = "Software Engineering"
        difficulty = "Beginner"

    elif any(word in text for word in [
        "ai",
        "artificial intelligence",
        "language model"
    ]):
        main_topic = "Artificial Intelligence"
        subtopics = [
            "Generative AI",
            "Machine Learning"
        ]
        context = "AI technology"
        apparent_interest = "Artificial Intelligence"
        difficulty = "Intermediate"

    elif any(word in text for word in [
        "laptop",
        "processor",
        "ram",
        "ssd",
        "gpu"
    ]):
        main_topic = "Technology Hardware"
        subtopics = [
            "Laptops",
            "Computer Hardware"
        ]
        context = "Technology hardware"
        apparent_interest = "Technology"
        difficulty = "Beginner"

    elif any(word in text for word in [
        "gaming",
        "game",
        "gaming pc"
    ]):
        main_topic = "Gaming Technology"
        subtopics = [
            "Gaming",
            "PC Hardware"
        ]
        context = "Gaming technology"
        apparent_interest = "Gaming"
        difficulty = "Beginner"

    else:
        main_topic = "General"
        subtopics = []
        context = "General content"
        apparent_interest = "Unknown"
        difficulty = "Beginner"

    return {
        "main_topic": main_topic,
        "subtopics": subtopics,
        "context": context,
        "apparent_interest": apparent_interest,
        "difficulty": difficulty
    }