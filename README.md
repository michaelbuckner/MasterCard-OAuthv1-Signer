# MasterCard-OAuthv1-Signer

This is a Flask application that provides an API for generating OAuth headers. It also provides an interface for uploading and managing certificate files, which are used in the OAuth process.

## Features

- Generate OAuth headers for authenticated requests to an API.
- Upload certificate files for use in OAuth requests.
- List uploaded certificate files.
- Healthcheck endpoint to ensure the service is running.

## Usage

The application provides several API endpoints:

- `/generate_oauth_headers` (POST): Generates OAuth headers for authenticated requests to an API.

- `/upload` (GET, POST): Provides a form for uploading certificate files.

- `/files` (GET): Displays a list of uploaded certificate files.

- `/api/upload_certificate` (POST): API endpoint for uploading a certificate.

- `/api/get_certificates` (GET): API endpoint for getting a list of uploaded certificates.

- `/healthcheck` (GET): Returns the status of the application.

## Contributing

Contributions to this project are welcome. Please submit a pull request or open an issue to discuss your proposed changes.

## License

This project is licensed under the MIT License.
