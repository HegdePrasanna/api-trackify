# api-trackify
API Trackify is a middleware package for FastAPI designed to log API calls and responses into a MongoDB database. It offers seamless integration to track and monitor API activities, allowing users to easily manage and analyze API usage within their applications.

## Installation
To install API Trackify, follow these steps:

1. Clone the repository:

    ```bash
    git clone https://github.com/HegdePrasanna/api-trackify.git
    cd api-trackify
    ```
2. Install the package:

    ```bash
    pip install .
    ```

## Usage

To use API Logger in your FastAPI application, follow these steps:

1. Import the APILogger class:
    ```python
    fastapilogger.apilogger_middleware import APILogger
    ```

2. Create an instance of the APILogger class and add it as middleware in your FastAPI app:
    ```python
    from fastapi import FastAPI

    app = FastAPI()

    # Replace these values with your MongoDB connection string and database name
    mongodb_connection_string = "your_mongodb_connection_string"
    database_name = "your_database_name"

    app.add_middleware(APILogger, mongodb_connection_string=mongodb_connection_string, database_name=database_name)
    ```

3. Customize the MongoDB connection string and database name according to your setup.

4. Run your FastAPI application.

## License
This project is licensed under the [MIT License](LICENSE).

## Contributing
Contributions are welcome! Please feel free to open issues or submit pull requests. If you encounter any issues or have suggestions for improvements, please create a GitHub issue or submit a pull request.

## Credits
API Trackify is developed and maintained by [Prasanna Hegde](https://github.com/HegdePrasanna) with the help of internet.

## Feedback
If you have any feedback, questions, or suggestions, please feel free to reach out to the project maintainers or open an issue on GitHub.
Enjoy !
