# FMHY Search - CrewAI Upgrade

## Overview

This is an upgraded version of the FMHY (FREEMEDIAHECKYEAH) Search application, enhanced with CrewAI multi-agent system for intelligent search capabilities.

## What's New

### CrewAI Integration

The application now features **3 specialized AI agents** that work together to provide enhanced search results:

1. **Content Indexer Agent**
   - Role: Organizes and categorizes FMHY wiki content
   - Expertise: Understanding wiki structure and content organization
   - Purpose: Efficiently categorizes search results by topic and type

2. **Search Analyzer Agent**
   - Role: Analyzes user search queries and interprets intent
   - Expertise: Natural language understanding and query interpretation
   - Purpose: Finds relevant content even with imprecise queries
   - Tools: BraveSearchTool for enhanced internet search

3. **Results Ranker Agent**
   - Role: Ranks and prioritizes search results
   - Expertise: Relevance scoring and result optimization
   - Purpose: Presents the most useful results first
   - Tools: BraveSearchTool for result verification and quality enhancement

### Features

- **AI-Enhanced Search**: When OpenAI API key is configured, the agents provide intelligent analysis of search results
- **Internet Search Integration**: BraveSearchTool enables agents to search the web for additional context
- **Smart Query Understanding**: Better interpretation of user intent with real-time web search
- **Contextual Results**: More relevant results based on semantic understanding and current web data
- **Ranked Results**: AI-powered ranking puts the best matches first
- **Result Analysis**: Get AI-generated insights about why results match your query
- **Enhanced Verification**: Results are verified against current web information using Brave Search

## Installation

### Prerequisites

- Python 3.8 or higher
- OpenAI API key (optional, for AI features)
- Brave Search API key (optional, for enhanced internet search via BraveSearchTool)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/colygon/fmhy-search-streamlit.git
   cd fmhy-search-streamlit
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set API Keys** (optional, for AI features)
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   export BRAVE_API_KEY="your-brave-api-key-here"
   ```

   Note: Get your Brave Search API key from [Brave Search API](https://brave.com/search/api/)

## Usage

### Run the Original Version
```bash
streamlit run fmhy-search.py
```

### Run the CrewAI Version
```bash
streamlit run fmhy_crewai.py
```

### Using AI Features

1. Set your OpenAI API key as an environment variable
2. (Optional) Set your Brave Search API key for enhanced internet search
3. Launch the CrewAI version
4. Enter your search query
5. Click "Search with CrewAI"
6. View AI analysis in the expandable section (for result sets with ≤50 items)
7. Agents will automatically use BraveSearchTool when additional context is needed

## Dependencies

### Core Dependencies
- `requests` - HTTP library for downloading wiki content
- `streamlit>=1.32.0` - Web application framework

### CrewAI Dependencies
- `crewai>=0.86.0` - Multi-agent orchestration framework
- `crewai_tools>=0.12.0` - CrewAI tools including BraveSearchTool
- `langchain-openai>=0.3.0` - OpenAI integration for language models

## Architecture

### Agent Workflow

```
User Query
    ↓
[Content Indexer] → Categorizes available content
    ↓
[Search Analyzer] → Interprets query intent + BraveSearchTool
    ↓
[Results Ranker] → Ranks and presents results + BraveSearchTool
    ↓
Enhanced Search Results
```

### BraveSearchTool Integration

The **BraveSearchTool** is integrated into the Search Analyzer and Results Ranker agents to provide:

- **Real-time web search**: Access to current information beyond the FMHY wiki
- **Context enhancement**: Additional context about tools, services, and resources
- **Verification**: Cross-reference FMHY results with current web data
- **Trend awareness**: Understand current popularity and relevance of tools
- **Alternative discovery**: Find similar or alternative resources

The tool is automatically invoked by agents when they need to:
- Clarify ambiguous queries
- Find current information about specific tools
- Verify if resources are still active
- Discover related tools or services

### Process

1. **Content Loading**: Wiki content is downloaded and indexed (cached for 12 hours)
2. **Basic Search**: Traditional keyword matching identifies candidate results
3. **AI Analysis** (if enabled): CrewAI agents analyze and enhance results
4. **Presentation**: Results are displayed with AI insights

## Technical Details

### Agent Configuration

- **LLM Model**: GPT-4O-Mini (fast and cost-effective)
- **Temperature**: 0.1 (focused, deterministic responses)
- **Process**: Sequential (agents work in order)
- **Delegation**: Disabled (each agent focuses on its specific task)
- **Tools**: BraveSearchTool (on Search Analyzer and Results Ranker agents)

### Performance

- Content caching: 12-hour TTL
- AI analysis: Only triggered for result sets ≤50 items
- Fallback: Works without API key (basic search only)

## Comparison: Original vs CrewAI

| Feature | Original | CrewAI Version |
|---------|----------|----------------|
| Basic keyword search | ✅ | ✅ |
| Multi-word queries | ✅ | ✅ |
| Result filtering | ✅ | ✅ |
| AI query understanding | ❌ | ✅ |
| Result analysis | ❌ | ✅ |
| Semantic search | ❌ | ✅ |
| Intelligent ranking | ❌ | ✅ |
| Internet search integration | ❌ | ✅ (BraveSearchTool) |
| Result verification | ❌ | ✅ (via Brave Search) |
| Works offline | ✅ | ✅ (basic mode) |

## Use Cases

### Best for CrewAI Version

- **Exploratory searches**: "What's the best way to..."
- **Vague queries**: When you don't know exact terminology
- **Category discovery**: Finding types of resources
- **Complex needs**: Multi-faceted requirements

### Best for Original Version

- **Exact matches**: You know the specific tool name
- **Fast searches**: No API latency
- **Offline use**: No internet required after initial load
- **Simple queries**: Direct keyword matches

## Configuration

### Environment Variables

```bash
# Required for AI features
OPENAI_API_KEY=sk-...

# Optional - for BraveSearchTool
BRAVE_API_KEY=your-brave-api-key

# Optional - Streamlit configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=localhost
```

### Customization

Edit `fmhy_crewai.py` to customize:

- Agent roles and behaviors (lines 228-266)
- LLM model selection (line 231)
- Cache duration (line 158)
- Result limits (line 415)

## Limitations

- AI features require OpenAI API key
- BraveSearchTool requires Brave Search API key (optional but recommended)
- AI analysis limited to ≤50 results (performance optimization)
- API costs apply for OpenAI and Brave Search usage
- Requires internet connection for wiki content and web search

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Credits

### Original Project
- **Author**: Rust1667
- **Repository**: [rust1667/fmhy-search-streamlit](https://github.com/rust1667/fmhy-search-streamlit)

### CrewAI Upgrade
- **Upgraded by**: Agent 23 (colygon)
- **Framework**: [CrewAI](https://github.com/joaomdmoura/crewAI)

### Data Source
- **FREEMEDIAHECKYEAH Wiki**: [fmhy.net](https://fmhy.net/)
- **Community**: r/FREEMEDIAHECKYEAH

## License

Same as original project. Please respect the FMHY community guidelines.

## Support

- **Issues**: [GitHub Issues](https://github.com/colygon/fmhy-search-streamlit/issues)
- **Original Project**: [rust1667/fmhy-search-streamlit](https://github.com/rust1667/fmhy-search-streamlit)
- **FMHY Discord**: [Discord Server](https://www.reddit.com/r/FREEMEDIAHECKYEAH/comments/17f8msf/public_discord_server/)

## Roadmap

### Potential Enhancements

- [ ] Memory system for learning user preferences
- [ ] Multi-turn conversations with agents
- [ ] Advanced semantic search with embeddings
- [ ] Category-specific specialized agents
- [ ] Result caching and personalization
- [ ] Alternative LLM support (Anthropic, local models)
- [ ] Query suggestion and autocomplete

## Version History

- **v2.1.0** (2025-12-17): Added BraveSearchTool for enhanced internet search
- **v2.0.0** (2025-12-17): CrewAI upgrade with 3 AI agents
- **v1.0.0**: Original version by Rust1667

---

**Agent 23 Mission Completed**: FMHY Search successfully upgraded with CrewAI multi-agent intelligence.
