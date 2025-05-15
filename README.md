# Codance - Neuromorphic Resonance Platform

## Detailed Description

**Overview:**

Codance is an AI-driven platform designed to create immersive, interactive dance experiences at scale. It establishes a symbiotic relationship between dancers, music, and artificial intelligence by integrating real-time movement tracking, biometric data from wearables, adaptive sound generation, haptic feedback, and dynamic visualizations. The system is built using Python, with FastAPI for the API layer, SQLAlchemy for database interaction, and a suite of machine learning and data processing libraries.

**Infrastructure & Core Technologies:**

*   **Web Framework:** FastAPI, with Uvicorn as the ASGI server.
*   **Database:** Utilizes SQLAlchemy as the ORM, suggesting a relational database backend (e.g., PostgreSQL, MySQL, SQLite). Database connection details are likely managed via `python-dotenv` and configuration files in `app/core/config.py`.
*   **Data Validation & Serialization:** Pydantic models are used extensively for request/response validation and schema definition.
*   **Authentication:** JWT-based authentication (`python-jose`) with password hashing (`passlib`, `bcrypt`).
*   **Machine Learning/Data Processing:** Leverages NumPy, Pandas, OpenCV, Scikit-learn, TensorFlow, PyTorch, and SciPy for various tasks including movement analysis, biometric data processing, and AI-driven sound/visualization generation.
*   **Asynchronous Operations:** FastAPI's async capabilities are used for non-blocking I/O operations.
*   **Modular Structure:** The application is organized into modules for different functionalities (users, movement, biometrics, sound, events, visualization), each with its own API routes, schemas, and models.

**Core Directory Structure:**

*   `codance/app/`: Main application code.
    *   `main.py`: FastAPI application entry point, middleware configuration, and router inclusion.
    *   `api/v1/`: Contains API router files for different modules.
    *   `core/`: Core components like database connection (`database.py`), authentication logic (`auth.py`), and configuration (`config.py`).
    *   `models/`: SQLAlchemy database model definitions.
    *   `schemas/`: Pydantic schema definitions for API request/response and data validation.
    *   `services/` (inferred): Likely contains business logic and service layer functions interacting with models and other components.
*   `codance/tests/`: Pytest-based automated tests.

**Core Classes and Models (SQLAlchemy & Pydantic):**

The system uses parallel structures for Pydantic schemas (data validation, API I/O) and SQLAlchemy models (database representation). Common patterns include `Base` (e.g., `UserBase`), `Create` (e.g., `UserCreate`), `Update` (e.g., `UserUpdate`), and display/database representation (e.g., `User`, `UserInDB`).

1.  **User Management (`user.py`)**
    *   **Models (`models/user.py`):**
        *   `User`: Stores user information (ID, email, username, hashed password, active status, admin status, timestamps). Relationships to `BiometricData`, `SongSelection`, `UserEvent`.
    *   **Schemas (`schemas/user.py`):**
        *   `UserBase`, `UserCreate`, `UserUpdate`, `UserInDB`, `User`: For user data.
        *   `Token`, `TokenData`: For authentication tokens.
    *   **Key Functionality:** User registration, login (token generation), fetching user details, updating user info, deleting users (admin).

2.  **Event Management (`event.py`)**
    *   **Models (`models/event.py`):**
        *   `Event`: Stores event details (ID, name, description, location, start/end times, active status, capacity, configuration, timestamps). Relationships to various data types like `UserEvent`, `MovementData`, `BiometricData`, etc.
        *   `UserEvent`: Links users to events (registration, check-in/out times, active status).
        *   `DetectedPattern`: Stores instances of detected movement patterns during an event (links to `MovementPattern` and `Event`, includes timestamp and confidence).
    *   **Schemas (`schemas/event.py`):**
        *   `EventBase`, `EventCreate`, `EventUpdate`, `Event`: For event data.
        *   `UserEventBase`, `UserEventCreate`, `UserEventUpdate`, `UserEvent`: For user-event association.
    *   **Key Functionality:** Creating, reading, updating, deleting events (admin); user registration for events, check-in/out.

3.  **Movement Tracking (`movement.py`)**
    *   **Models (`models/movement.py`):**
        *   `MovementData`: Stores raw or processed movement data (ID, event ID, timestamp, data type, coordinates (JSON), velocity, acceleration, crowd density, intensity). Relationships to `Event` and `SoundEvent`.
        *   `MovementPattern`: Defines recognizable movement patterns (ID, name, description, pattern data (JSON), timestamps). Relationship to `DetectedPattern`.
    *   **Schemas (`schemas/movement.py`):**
        *   `MovementDataBase`, `MovementDataCreate`, `MovementDataUpdate`, `MovementData`: For movement data records.
        *   `MovementPatternBase`, `MovementPatternCreate`, `MovementPatternUpdate`, `MovementPattern`: For defining movement patterns.
        *   `DetectedPatternBase`, `DetectedPatternCreate`, `DetectedPattern`: For logged detected patterns.
    *   **Key Functionality:** Storing movement data, defining and detecting movement patterns. Includes a simulation endpoint.

4.  **Biometric System (`biometrics.py`)**
    *   **Models (`models/biometrics.py`):**
        *   `BiometricData`: Stores biometric readings (ID, user ID, event ID, device ID, timestamp, heart rate, GSR, temperature, energy level, emotional state). Relationships to `User` and `Event`.
        *   `BiometricDevice`: Information about registered biometric devices (ID, device ID, type, active status, timestamps).
    *   **Schemas (`schemas/biometrics.py`):**
        *   `BiometricDataBase`, `BiometricDataCreate`, `BiometricDataUpdate`, `BiometricData`: For biometric data records.
        *   `BiometricDeviceBase`, `BiometricDeviceCreate`, `BiometricDeviceUpdate`, `BiometricDevice`: For biometric device management.
    *   **Key Functionality:** Storing biometric data from users during events, managing biometric devices. Includes a simulation endpoint.

5.  **Sound Engine (`sound.py`)**
    *   **Models (`models/sound.py`):**
        *   `SoundEvent`: Records generated sound events (ID, event ID, optional movement data ID, timestamp, sound type, parameters (JSON), duration, intensity). Relationships to `Event` and `MovementData`.
        *   `SongSelection`: User-selected songs for an event (ID, user ID, event ID, title, artist, duration, audio features (JSON), approval status, timestamp). Relationships to `User` and `Event`.
        *   `SoundSample`: Stores sound samples (ID, name, category, binary sample data, duration, sample rate, timestamp).
        *   `SoundPreset`: Predefined sound configurations (ID, name, description, parameters (JSON), timestamps).
    *   **Schemas (`schemas/sound.py`):**
        *   `SoundEventBase`, `SoundEventCreate`, `SoundEventUpdate`, `SoundEvent`: For sound event data.
        *   `SongSelectionBase`, `SongSelectionCreate`, `SongSelectionUpdate`, `SongSelection`: For song selection data.
        *   `SoundSampleBase`, `SoundSampleCreate`, `SoundSample`: For sound sample management.
        *   `SoundPresetBase`, `SoundPresetCreate`, `SoundPresetUpdate`, `SoundPreset`: For sound preset management.
    *   **Key Functionality:** Generating sound events (potentially linked to movement), managing user song selections, storing sound samples and presets. Includes a simulation endpoint for sound events.

6.  **Visualization (`visualization.py`)**
    *   **Models (`models/visualization.py`):**
        *   `VisualizationEvent`: Records generated visualization events (ID, event ID, timestamp, type, parameters (JSON), duration, intensity). Relationship to `Event`.
        *   `VisualizationPreset`: Predefined visualization configurations (ID, name, description, parameters (JSON), timestamps).
    *   **Schemas (`schemas/visualization.py`):**
        *   `VisualizationEventBase`, `VisualizationEventCreate`, `VisualizationEventUpdate`, `VisualizationEvent`: For visualization event data.
        *   `VisualizationPresetBase`, `VisualizationPresetCreate`, `VisualizationPresetUpdate`, `VisualizationPreset`: For visualization preset management.
    *   **Key Functionality:** Generating visualization events, managing visualization presets. Includes a simulation endpoint.

**API Endpoints (`codance/app/api/v1/`):**

The API is versioned under `/api/v1/`. Each module has a set of CRUD-like (Create, Read, Update, Delete) endpoints for its respective resources. Most endpoints require authentication (`get_current_active_user`) and some are restricted to admin users (`get_current_admin_user`).

*   **Root & Health:**
    *   `GET /`: Basic API information.
    *   `GET /health`: Health check.

*   **Users (`/users`)**:
    *   `POST /token`: Login and get access token.
    *   `GET /me`: Get current authenticated user's details.
    *   `POST /register`: Register a new user.
    *   `POST /`: Create a new user (admin).
    *   `GET /`: List all users (admin).
    *   `GET /{user_id}`: Get specific user details.
    *   `PUT /{user_id}`: Update user details.
    *   `DELETE /{user_id}`: Delete a user (admin).

*   **Movement Tracking (`/movement`)**:
    *   `/data`: CRUD operations for `MovementData` records.
    *   `/patterns`: CRUD operations for `MovementPattern` definitions (admin for CUD).
    *   `/detected-patterns`: CRUD for `DetectedPattern` instances.
    *   `POST /simulate`: Simulate movement data for an event.

*   **Biometric Data (`/biometrics`)**:
    *   `/data`: CRUD operations for `BiometricData` records (users can manage their own data; CUD restricted).
    *   `/devices`: CRUD operations for `BiometricDevice` registration (admin for CUD).
    *   `POST /simulate`: Simulate biometric data for a user at an event.

*   **Sound Generation (`/sound`)**:
    *   `/events`: CRUD operations for `SoundEvent` records (admin for delete).
    *   `/songs`: CRUD operations for `SongSelection` (users can manage their selections, admin can approve/manage all).
    *   `/samples`: (Assumed based on schema/model, might be admin-only for upload/management - *router details not fully parsed for this sub-entity*).
    *   `/presets`: CRUD operations for `SoundPreset` definitions (admin for CUD).
    *   `POST /simulate`: Simulate a sound event.

*   **Event Management (`/events`)**:
    *   `/`: CRUD operations for `Event` definitions (admin for CUD).
    *   `GET /upcoming`: Get upcoming events.
    *   `/register`: Register current user for an event. Admin can register others.
    *   `/registrations`: CRUD operations for `UserEvent` (event registrations).
    *   `/checkin`, `/checkout`: Endpoints for user check-in/out at events.

*   **Visualization (`/visualization`)**:
    *   `/events`: CRUD operations for `VisualizationEvent` records (admin for delete).
    *   `/presets`: CRUD operations for `VisualizationPreset` definitions (admin for CUD).
    *   `POST /simulate`: Simulate a visualization event.

## Getting Started

### Prerequisites

- Python 3.9+
- Required packages (see requirements.txt)

### Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/codance.git
cd codance
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run the development server
```bash
uvicorn app.main:app --reload
```

4. Visit http://localhost:8000/docs for API documentation

## API Endpoints

The Codance API provides endpoints for:
- Movement tracking data ingestion
- Biometric data processing
- Sound generation based on movement patterns
- User management and preferences
- Event configuration and management

## Testing

Run the test suite:
```bash
pytest
```
