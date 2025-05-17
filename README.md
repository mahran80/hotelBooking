


# hotelBooking
full functionality hotel booking app created with django rest framework in backend and html css javascript in frontend 

 project in master branch 

## Features

- **User Authentication:** Register, login, logout, and profile management.
- **Event & Room Management:** Admins can create, update, and delete events and rooms.
- **Booking System:** Users can book events/rooms, view their bookings, and manage tickets.
- **Admin Panel:** Accessible only to staff users for full CRUD operations.
- **Multi-language Support:** English and Arabic (switchable in the navbar).
- **Role-based Permissions:** Only staff can access admin features.
- **Responsive Web UI:** Modern navigation, dark mode, and language switcher.

---

## Project Structure

```
hottelBooking/
├── backend/
│   ├── booking/
│   │   ├── base/
│   │   ├── room_booking/
│   │   ├── templates/
│   │   ├── locale/
│   │   ├── manage.py
│   │   └── ...
│   └── requirements.txt


---

## Getting Started

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- (Recommended) Virtualenv

---

### Backend Setup

1. **Clone the repository**
   ```sh
   git clone <your-repo-url>
   cd hottelBooking/backend/booking
   ```

2. **Create and activate a virtual environment**
   ```sh
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # or
   source venv/bin/activate  # On Mac/Linux
   ```

3. **Install dependencies**
   ```sh
   pip install -r ../requirements.txt
   ```

4. **Apply migrations**
   ```sh
   python manage.py migrate
   ```

5. **Create a superuser (admin account)**
   ```sh
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```sh
   python manage.py runserver
   ```

7. **Access the site**
   - Main site: [http://localhost:8000/](http://localhost:8000/)
   - Admin panel: [http://localhost:8000/admin/](http://localhost:8000/admin/)

---

### Multi-language Support

- Switch languages using the globe icon in the navbar.
- To update or add translations:
  ```sh
  python manage.py makemessages -l ar
  python manage.py compilemessages
  ```

---

### Functionality

- **Users:** Register, login, book events/rooms, view and manage their bookings.
- **Admins:** Access the admin panel, manage events, rooms, categories, and users.
- **Navbar:** Admin button appears only for staff users.
- **Dark Mode:** Toggle with the moon icon in the navbar.
- **Language:** Switch between English and Arabic.

---

### Notes

- By default, the backend uses SQLite for development.
- CORS is configured for frontend development at `localhost:3000`.
- For production, set `DEBUG=False` and configure `ALLOWED_HOSTS` in `settings.py`.

---

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License.

---



