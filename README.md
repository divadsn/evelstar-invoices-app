# Evelstar Invoices App

A simple Python Tkinter application to automate the process of uploading invoices to the Evelstar courier portal.

## Why This Project?

I created this project because I found the new invoice upload form frustrating. The REGON API integration occasionally fails, causing issues with pre-filled fields. With Azure Document Intelligence available, I wanted to automate invoice transcription for a smoother experience.

In the future, I plan to add more features, such as:
- A calculator for determining the flat-rate tax (ryczałt) payments.
- A tool for summing up all cash payouts from Glovo.

## How the API Works
> [!WARNING]
> This project is intended to add value by automating the process of uploading invoices to the Evelstar courier portal.
> It is **not** intended to abuse or overload the Evelstar API.
> Please use this application responsibly and in accordance with Evelstar's terms of service.

To ensure flexibility and avoid hardcoding credentials, I developed a method to extract Firebase configuration dynamically from the portal's JavaScript code. All HTTP requests used in this project were reverse-engineered by analyzing the website’s network activity.

The API has two main components:
1. **Firebase Client** – Handles authentication and token management for secure API access.
2. **API Client** – Interfaces with the Evelstar API to upload invoices and retrieve relevant data.

All the relevant code can be found in the [`invoices_app.api`](./invoices_app/api) module.
