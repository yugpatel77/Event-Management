<<<<<<< HEAD
# 360 Degree Venue and Event Management

**Where luxury and planning meets**

A comprehensive event planning platform with 360-degree virtual venue tours, professional event management services, and seamless vendor coordination.

## 🎯 Project Overview

360 Degree Venue and Event Management is a smart event booking platform that connects users with professional event managers and premium venues. The platform features immersive 360-degree virtual tours, comprehensive vendor management, and personalized event planning services.

### Target Users

1. **Regular Users** - Event organizers seeking professional assistance
2. **Event Managers** - Real professionals providing expert event planning services
3. **Administrators** - Platform managers overseeing operations and quality control

### Key Features

- **360-Degree Virtual Venue Tours** - Immersive venue exploration
- **Professional Event Management** - Real event managers, not AI
- **Vendor Management** - Food, DJ, Sports, Music, Cooking, Adventure services
- **Secure Payment Processing** - Integrated payment solutions
- **Real-time Communication** - Direct messaging with event managers
- **Comprehensive Booking System** - End-to-end event management

## 🛠 Technology Stack

- **Backend**: Django 4.2+
- **Frontend**: Django Templates + JavaScript
- **Database**: MySQL 8.0+
- **Payment**: Stripe/PayPal integration
- **Maps**: Google Maps API
- **360 Tours**: Pannellum.js
- **Deployment**: AWS/DigitalOcean with Docker

## 🚀 Quick Start

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up MySQL database
4. Run migrations: `python manage.py migrate`
5. Create superuser: `python manage.py createsuperuser`
6. Start development server: `python manage.py runserver`

## 📁 Project Structure

```
event_manager/
├── manage.py
├── requirements.txt
├── event_manager/          # Main project settings
├── users/                  # User authentication & profiles
├── venues/                 # Venue management & 360 tours
├── events/                 # Event booking & management
├── managers/               # Event manager profiles & services
├── vendors/                # Vendor management (food, DJ, etc.)
├── payments/               # Payment processing
├── communications/         # Messaging & consultations
├── static/                 # Static files (CSS, JS, images)
├── templates/              # HTML templates
└── docs/                   # Documentation
```

## 🔐 Security Features

- Role-based access control
- Secure authentication
- Payment data encryption
- CSRF protection
- SQL injection prevention
- XSS protection

## 📊 Database Schema

The platform uses a comprehensive MySQL schema with proper relationships between:
- Users and their profiles
- Event managers and verification status
- Venues and 360-degree tour data
- Events and bookings
- Vendors and services
- Payments and transactions

## 🎨 UI/UX Features

- Responsive design for all devices
- Modern, luxury-focused interface
- Intuitive navigation
- Interactive 360-degree tours
- Real-time chat interface
- Professional dashboard layouts

## 📈 Future Enhancements

- Mobile app development
- AI-powered venue recommendations
- Advanced analytics dashboard
- Multi-language support
- Integration with social media platforms

## 🤝 Contributing

Please read our contributing guidelines before submitting pull requests.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details. 
=======
# Event-Management
It is manage diffrent types of events...
>>>>>>> 049ecb13c4fa9207781cdec1686c30a1bdf4c2ba
