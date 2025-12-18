"""
FMHY Search with CrewAI
Upgraded version with intelligent search agents
"""

import streamlit as st
import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import BraveSearchTool
from langchain_openai import ChatOpenAI
import requests
import base64
import re

# Streamlit page configuration
st.set_page_config(
    page_title="FMHY Search with CrewAI",
    page_icon="https://i.imgur.com/s9abZgP.png",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://github.com/colygon/fmhy-search-streamlit',
        'Report a bug': "https://github.com/colygon/fmhy-search-streamlit/issues",
        'About': "https://github.com/colygon/fmhy-search-streamlit - Upgraded with CrewAI"
    }
)

st.title("Search FMHY with CrewAI")
st.caption("Powered by intelligent search agents")

with st.sidebar:
    st.image("https://i.imgur.com/s9abZgP.png", width=100)
    st.text("AI-Enhanced Search Engine for r/FREEMEDIAHECKYEAH")
    st.markdown("### Links:")
    st.markdown("* Wiki: [Reddit](https://www.reddit.com/r/FREEMEDIAHECKYEAH/wiki/index/), [.net](https://fmhy.net/)")
    st.markdown("* [Github Repo](https://github.com/colygon/fmhy-search-streamlit)")
    st.markdown("* [Other Search Tools](https://www.reddit.com/r/FREEMEDIAHECKYEAH/comments/105xraz/howto_search_fmhy/)")
    st.markdown("---")
    st.markdown("### CrewAI Agents:")
    st.markdown("* Content Indexer Agent")
    st.markdown("* Search Analyzer Agent (BraveSearch)")
    st.markdown("* Results Ranker Agent (BraveSearch)")
    st.markdown("---")
    st.markdown("### Tools:")
    st.markdown("* BraveSearchTool for enhanced internet search")

# API Key configuration
openai_api_key = os.getenv("OPENAI_API_KEY", "")
if not openai_api_key:
    with st.sidebar:
        st.warning("Set OPENAI_API_KEY environment variable for AI features")

# ----------------Base64 page processing------------
def fix_base64_string(encoded_string):
    missing_padding = len(encoded_string) % 4
    if missing_padding != 0:
        encoded_string += '=' * (4 - missing_padding)
    return encoded_string

def decode_base64_in_backticks(input_string):
    def base64_decode(match):
        encoded_data = match.group(0)[1:-1]
        decoded_bytes = base64.b64decode(fix_base64_string(encoded_data))
        try:
            return decoded_bytes.decode()
        except:
            return encoded_data

    pattern = r"`[^`]+`"
    decoded_string = re.sub(pattern, base64_decode, input_string)
    return decoded_string

def remove_empty_lines(text):
    lines = text.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    return '\n'.join(non_empty_lines)

def extract_base64_sections(base64_page):
    sections = base64_page.split("***")
    formatted_sections = []
    for section in sections:
        formatted_section = remove_empty_lines(
            section.strip().replace("#### ", "").replace("\n\n", " - ").replace("\n", ", ")
        )
        formatted_section = decode_base64_in_backticks(formatted_section)
        formatted_section = '[Base64](https://rentry.co/FMHYBase64) > ' + formatted_section
        formatted_sections.append(formatted_section)
    return formatted_sections

# ----------------Content Processing------------
def addPretext(lines, icon, baseURL, subURL):
    modified_lines = []
    currMdSubheading = ""
    currSubCat = ""
    currSubSubCat = ""

    for line in lines:
        if line.startswith("#"):
            if not subURL == "storage":
                if line.startswith("# >"):
                    currMdSubheading = "#" + line.replace("# >", "").strip().replace(" / ", "-").replace(" ", "-").lower()
                    currSubCat = "/ " + line.replace("# >", "").strip() + " "
                    currSubSubCat = ""
                elif line.startswith("## >"):
                    if not subURL == "non-english":
                        currMdSubheading = "#" + line.replace("## >", "").strip().replace(" / ", "-").replace(" ", "-").lower()
                    currSubSubCat = "/ " + line.replace("## >", "").strip() + " "
            elif subURL == "storage":
                if line.startswith("## "):
                    currMdSubheading = "#" + line.replace("## ", "").strip().replace(" / ", "-").replace(" ", "-").lower()
                    currSubCat = "/ " + line.replace("## ", "").strip() + " "
                    currSubSubCat = ""
                elif line.startswith("### "):
                    currMdSubheading = "#" + line.replace("### ", "").strip().replace(" / ", "-").replace(" ", "-").lower()
                    currSubSubCat = "/ " + line.replace("### ", "").strip() + " "

            if 'http' in currSubCat: currSubCat = ''
            if 'http' in currSubSubCat: currSubSubCat = ''

        elif any(char.isalpha() for char in line):
            preText = f"[{icon}{currSubCat}{currSubSubCat}]({baseURL}{subURL}{currMdSubheading}) > "
            if line.startswith("* "): line = line[2:]
            modified_lines.append(preText + line)

    return modified_lines

def dlWikiChunk(fileName, icon, redditSubURL):
    if fileName == 'NSFWPiracy.md':
        page = requests.get("https://rentry.co/freemediafuckyeah/raw").text.replace("\r", "")
    elif not fileName == 'base64.md':
        page = requests.get(f"https://raw.githubusercontent.com/fmhy/edit/refs/heads/main/docs/{fileName.lower()}").text
    elif fileName == 'base64.md':
        page = requests.get("https://rentry.co/FMHYB64/raw").text.replace("\r", "")

    baseURL = "https://fmhy.net/"
    if not fileName == 'base64.md':
        subURL = fileName.replace(".md", "").lower()
        lines = page.split('\n')
        lines = addPretext(lines, icon, baseURL, subURL)
    elif fileName == 'base64.md':
        lines = extract_base64_sections(page)

    return lines

@st.cache_resource(ttl=43200)
def alternativeWikiIndexing():
    wikiChunks = [
        dlWikiChunk("video.md", "Video", "video"),
        dlWikiChunk("ai.md", "AI", "ai"),
        dlWikiChunk("mobile.md", "Mobile", "android"),
        dlWikiChunk("audio.md", "Audio", "audio"),
        dlWikiChunk("downloading.md", "Download", "download"),
        dlWikiChunk("educational.md", "Education", "edu"),
        dlWikiChunk("gaming.md", "Gaming", "games"),
        dlWikiChunk("privacy.md", "Privacy", "adblock-vpn-privacy"),
        dlWikiChunk("system-tools.md", "System", "system-tools"),
        dlWikiChunk("file-tools.md", "Files", "file-tools"),
        dlWikiChunk("internet-tools.md", "Internet", "internet-tools"),
        dlWikiChunk("social-media-tools.md", "Social", "social-media"),
        dlWikiChunk("text-tools.md", "Text", "text-tools"),
        dlWikiChunk("video-tools.md", "Video Tools", "video-tools"),
        dlWikiChunk("misc.md", "Misc", "misc"),
        dlWikiChunk("reading.md", "Reading", "reading"),
        dlWikiChunk("torrenting.md", "Torrenting", "torrent"),
        dlWikiChunk("img-tools.md", "Images", "img-tools"),
        dlWikiChunk("gaming-tools.md", "Gaming Tools", "gaming-tools"),
        dlWikiChunk("linux-macos.md", "Linux/macOS", "linux"),
        dlWikiChunk("developer-tools.md", "Developer", "dev-tools"),
        dlWikiChunk("non-english.md", "Non-English", "non-eng"),
        dlWikiChunk("storage.md", "Storage", "storage")
    ]
    return [item for sublist in wikiChunks for item in sublist]

# ----------------Search Functions------------
def removeEmptyStringsFromList(stringList):
    return [string for string in stringList if string != '']

def checkWordForWordMatch(line, searchQuery):
    lineWords = removeEmptyStringsFromList(
        line.lower().replace('[', ' ').replace(']', ' ').split(' ')
    )
    lineWords = [element.strip() for element in lineWords]
    searchQueryWords = removeEmptyStringsFromList(searchQuery.lower().split(' '))

    for word in searchQueryWords:
        if word not in lineWords:
            return False
    return True

def getLinesThatContainAllWords(lineList, searchQuery):
    words = removeEmptyStringsFromList(searchQuery.lower().split(' '))
    bumped = []
    for line in lineList:
        lineModded = line.lower()
        if all(word in lineModded for word in words):
            bumped.append(line)
    return bumped

def filterLines(lineList, searchQuery):
    if len(searchQuery) <= 2 or (searchQuery == searchQuery.upper() and len(searchQuery) <= 5):
        return [line for line in lineList if checkWordForWordMatch(line, searchQuery)]
    else:
        return getLinesThatContainAllWords(lineList, searchQuery)

def moveBetterMatchesToFront(myList, searchQuery):
    bumped = []
    notBumped = []
    for element in myList:
        if checkWordForWordMatch(element, searchQuery):
            bumped.append(element)
        else:
            notBumped.append(element)
    return bumped + notBumped

# ----------------CrewAI Agents------------
@st.cache_resource
def create_search_crew():
    """Create the CrewAI search crew with 3 specialized agents"""

    llm = None
    if openai_api_key:
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1, api_key=openai_api_key)

    # Initialize BraveSearchTool for enhanced internet search
    brave_search = BraveSearchTool()

    # Agent 1: Content Indexer - Organizes and categorizes content
    content_indexer = Agent(
        role='Content Indexer',
        goal='Organize and categorize FMHY wiki content for efficient searching',
        backstory="""You are an expert at organizing large amounts of information.
        You understand the FMHY wiki structure and can identify relevant categories
        and sections based on user queries.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

    # Agent 2: Search Analyzer - Interprets user queries and finds relevant content
    search_analyzer = Agent(
        role='Search Analyzer',
        goal='Analyze user search queries and identify the most relevant content matches',
        backstory="""You are a search specialist who understands user intent.
        You can interpret queries, identify synonyms, and find the most relevant
        results even when the query doesn't exactly match the content. You have access
        to internet search to supplement FMHY wiki content with additional context.""",
        verbose=True,
        allow_delegation=False,
        tools=[brave_search],
        llm=llm
    )

    # Agent 3: Results Ranker - Ranks and presents results optimally
    results_ranker = Agent(
        role='Results Ranker',
        goal='Rank search results by relevance and present them in the most useful way',
        backstory="""You are an expert at ranking search results by relevance.
        You understand what makes a result valuable to users and can prioritize
        exact matches, contextual relevance, and user intent. You can use internet
        search to verify and enhance result quality.""",
        verbose=True,
        allow_delegation=False,
        tools=[brave_search],
        llm=llm
    )

    return content_indexer, search_analyzer, results_ranker

# ----------------Main Search Function------------
def doCrewAISearch(searchInput, lineList):
    """Perform search using CrewAI agents"""

    searchInput = searchInput.strip()

    if searchInput == "":
        st.warning("The search query is empty.", icon="Warning")
        return

    # Basic filtering
    linesFound = filterLines(lineList, searchInput)

    # Rank results
    linesFound = moveBetterMatchesToFront(linesFound, searchInput)

    # Show results count
    if len(linesFound) > 300:
        st.warning(f"Too many results ({len(linesFound)}). Showing top 300 full-word matches.", icon="Info")
        linesFound = [line for line in linesFound if checkWordForWordMatch(line, searchInput)][:300]

    if len(linesFound) > 700:
        st.warning(f"Too many results ({len(linesFound)}). Please refine your search.", icon="Warning")
        return

    # Display results
    if len(linesFound) > 0:
        st.text(f"{len(linesFound)} search results for '{searchInput}':\n")

        # If CrewAI is available, use agents for enhanced analysis
        if openai_api_key and len(linesFound) <= 50:
            with st.expander("AI Analysis (Powered by CrewAI)", expanded=False):
                try:
                    content_indexer, search_analyzer, results_ranker = create_search_crew()

                    # Create tasks for the agents
                    analyze_task = Task(
                        description=f"""Analyze the search query '{searchInput}' and the following results.
                        Identify the main categories and types of resources found.
                        Results preview: {linesFound[:5]}""",
                        expected_output="Brief categorization of results and main themes found",
                        agent=search_analyzer
                    )

                    rank_task = Task(
                        description=f"""Based on the query '{searchInput}', explain why these results are relevant
                        and suggest which ones are likely most useful to the user.""",
                        expected_output="Ranking explanation and recommendations",
                        agent=results_ranker
                    )

                    crew = Crew(
                        agents=[search_analyzer, results_ranker],
                        tasks=[analyze_task, rank_task],
                        process=Process.sequential,
                        verbose=False
                    )

                    with st.spinner("AI agents analyzing results..."):
                        result = crew.kickoff()
                        st.info(str(result), icon="Info")

                except Exception as e:
                    st.error(f"AI analysis unavailable: {str(e)}")

        # Display results
        textToPrint = "\n\n".join(linesFound)
        st.markdown(textToPrint)

        if len(linesFound) > 0 and len(linesFound) <= 10:
            with st.expander("Not what you were looking for?"):
                st.info(
                    "For specific media or software, try a [CSE](https://fmhy.net/internet-tools#custom-search-engines) / "
                    "Live Sports [here](https://fmhy.net/videopiracyguide#live-tv-sports) / "
                    "Ask in [Discord](https://www.reddit.com/r/FREEMEDIAHECKYEAH/comments/17f8msf/public_discord_server/)",
                    icon="Info"
                )
    else:
        st.markdown(f"No results found for '{searchInput}'!")
        st.info(
            "For specific media or software, try a [CSE](https://fmhy.net/internet-tools#custom-search-engines) / "
            "Live Sports [here](https://fmhy.net/videopiracyguide#live-tv-sports) / "
            "Ask in [Discord](https://www.reddit.com/r/FREEMEDIAHECKYEAH/comments/17f8msf/public_discord_server/)",
            icon="Info"
        )

# ----------------Main App------------
# Initialize the wiki index
with st.spinner("Loading FMHY wiki content..."):
    lineList = alternativeWikiIndexing()

st.success(f"Loaded {len(lineList)} entries from FMHY wiki", icon="Success")

# Search interface
queryInputFromBox = st.text_input(
    label="Search Query",
    value="",
    help="Search for links in the FMHY Wiki. Use multiple words for better results.",
    placeholder="e.g. 'streaming movies' or 'ad blocker'"
)

if st.button("Search with CrewAI", type="primary"):
    queryInput = queryInputFromBox
    doCrewAISearch(queryInput, lineList)
