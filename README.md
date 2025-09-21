# Zaki: AI Agent Manager for Real Estate and Construction

## Project Overview and Use Cases

**Zaki** is an intelligent, modular AI agent system designed to automate high-friction, repetitive workflows in the construction, real estate, and property management industries. Zaki combines large language models (LLMs), vision models, and system-level integrations to operate as a proactive digital employee across multiple domains—offering speed, clarity, and operational efficiency where traditional systems fall short.

Zaki is not a single AI model, but a multi-agent architecture composed of microservices, each responsible for solving a specific pain point in real-world project workflows.

### Key Use Cases

#### 1. RFI Summarizer
- **Problem**: RFIs (Requests for Information) often arrive as long, unstructured emails or PDFs. Engineers and architects spend 15–20 minutes manually reading, interpreting, and summarizing each request.
- **Solution**: Parses RFI emails or PDFs, summarizes the key question, requester, and referenced drawings, then logs to database and forwards to correct discipline lead.

#### 2. Daily Site Report Generator
- **Problem**: Site managers manually create daily reports covering weather, manpower, progress, and safety issues, often delayed or inaccurate.
- **Solution**: Accepts photo uploads and bullet-point updates via web form, generates narrative daily reports using LLM, outputs Word/PDF files.

#### 3. Material Order Optimizer
- **Problem**: Manual material ordering relies on outdated spreadsheets and guesswork, leading to overstocking or stockouts.
- **Solution**: Reads material usage history and project schedule, forecasts needs using LLM-enhanced logic, outputs purchase orders.

#### 4. Safety Compliance Checker
- **Problem**: Safety officers manually review site images for PPE compliance, inefficient for multiple sites.
- **Solution**: Ingests site images, uses vision models to detect PPE violations, triggers alerts and logs violations.

## Tech Stack

### Backend Technologies
- **FastAPI**: RESTful API framework for backend services
- **Python**: Core programming language
- **Uvicorn**: ASGI server for running FastAPI applications

### Frontend Technologies
- **Streamlit**: Interactive web interface for user interactions
- **HTML/CSS**: Web interface components

### AI/ML Technologies
- **Hugging Face Transformers**: Large Language Model integration
- **Google Gemma-2-2b-it**: Text generation and summarization model
- **Vision Models**: For image analysis and PPE compliance checking

### Document Processing
- **PDFPlumber**: PDF text extraction and processing
- **Python-docx**: Word document generation
- **Pillow**: Image processing and manipulation

### Data Storage & Communication
- **Logging**: Comprehensive system logging for debugging
- **File System**: Local file storage with organized directory structure
- **API Integration**: RESTful API communication between services

### Dependencies
```
requests
python-docx
pillow
fastapi
uvicorn
pdfplumber
streamlit
python-multipart
```

## Dataset

The system processes various types of construction and real estate data:

### Input Data Types
- **RFI Documents**: PDF files containing Requests for Information from construction projects
- **Site Images**: JPEG/PNG photos from construction sites for progress tracking and safety compliance
- **Daily Report Data**: 
  - Weather conditions
  - Manpower information
  - Progress updates
  - Safety observations
  - Date/time stamps

### Sample Data
- **RFI.pdf**: Sample RFI document for testing the summarization feature
- **Log Files**: System logs stored in `zaki.log` for debugging and monitoring
- **Generated Reports**: Output Word documents stored in `not_needed` directory

### Data Flow
1. **Input**: Users upload PDFs, images, or enter form data through Streamlit interface
2. **Processing**: FastAPI backend processes data using AI models
3. **Output**: Generated summaries, reports, and documents downloadable by users

## Progress

### Completed Features ✅
- [x] **RFI Summarizer**: Complete PDF parsing and AI-powered summarization
- [x] **Daily Site Report Generator**: Full workflow from data input to Word document generation
- [x] **Web Interface**: Streamlit-based user interface with multiple tools
- [x] **FastAPI Backend**: RESTful API endpoints for all core services
- [x] **Document Processing**: PDF text extraction and Word document generation
- [x] **Image Handling**: Photo upload and processing capabilities
- [x] **Logging System**: Comprehensive error tracking and debugging

### In Development 🚧
- [ ] **Material Order Optimizer**: LLM-enhanced material forecasting
- [ ] **Safety Compliance Checker**: Vision model for PPE detection
- [ ] **Environmental Impact Reporter**: ESG compliance reporting
- [ ] **Tenant Auto-Responder**: Automated property management responses

### Planned Features 📋
- [ ] **Voice Command Interface**: Field worker interaction via voice
- [ ] **Multi-language Support**: Arabic and regional language integration
- [ ] **Real-time Data Sync**: IoT sensors and ERP system integration
- [ ] **Agent Memory & Learning**: Vector stores and RAG implementation
- [ ] **API Marketplace**: Third-party plugin architecture

## View Link

### Local Development
To run the application locally:

1. **Install Dependencies**:
   ```bash
   pip install requests python-docx pillow fastapi uvicorn pdfplumber streamlit python-multipart
   ```

2. **Start Backend Server**:
   ```bash
   cd Zaki
   uvicorn main:app --reload
   ```
   Backend will be available at: `http://localhost:8000`

3. **Start Frontend Interface** (in new terminal):
   ```bash
   cd Zaki
   streamlit run ui_app.py
   ```
   Frontend will be available at: `http://localhost:8501`

### API Documentation
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Testing the Application
- **RFI Summarizer**: Upload the provided `RFI.pdf` file
- **Report Generator**: Enter sample data and upload any JPEG/PNG image

## Contribution

We welcome contributions to the Zaki project! Here's how you can get involved:

### Getting Started
1. **Fork the repository**
2. **Clone your fork**: `git clone https://github.com/your-username/Zaki---AI-Agent.git`
3. **Create a feature branch**: `git checkout -b feature/your-feature-name`
4. **Set up development environment** following the installation instructions above

### Development Guidelines
- Follow Python PEP 8 style guidelines
- Add comprehensive logging for new features
- Test all new functionality with sample data
- Update documentation for any API changes
- Ensure compatibility with existing microservices architecture

### Areas for Contribution
- **New Task Modules**: Implement additional AI-powered construction/real estate tools
- **UI/UX Improvements**: Enhance Streamlit interface design and usability
- **AI Model Integration**: Add new LLM or vision model capabilities
- **Performance Optimization**: Improve processing speed and memory usage
- **Documentation**: Improve code documentation and user guides
- **Testing**: Add unit tests and integration tests

### Submitting Changes
1. **Commit changes**: `git commit -m "Description of changes"`
2. **Push to branch**: `git push origin feature/your-feature-name`
3. **Create Pull Request** with detailed description of changes
4. **Respond to code review feedback**

### Code of Conduct
- Be respectful and constructive in all interactions
- Focus on building solutions that benefit the construction and real estate industries
- Maintain high code quality and documentation standards

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

### MIT License Summary
- ✅ **Commercial use** allowed
- ✅ **Modification** allowed  
- ✅ **Distribution** allowed
- ✅ **Private use** allowed
- ❗ **License and copyright notice** required
- ❗ **No warranty** provided

---

**Built with ❤️ for the Construction and Real Estate Industry**
