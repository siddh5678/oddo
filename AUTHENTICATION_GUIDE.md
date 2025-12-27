# Authentication & Database Guide

## 🗄️ Database Setup

GearGuard+ now uses **SQLite database** for data persistence. The database file `gearguard.db` will be automatically created when you first run the application.

### Database Features

- **SQLite**: Lightweight, file-based database (no server needed)
- **Automatic Setup**: Tables are created automatically on first run
- **Data Persistence**: All data is saved to database file

### Database Tables

1. **users** - User accounts for authentication
2. **employees** - Employee/Technician records
3. **maintenance_teams** - Maintenance team information
4. **team_technicians** - Many-to-many relationship (teams ↔ technicians)
5. **equipment** - Equipment/Asset records
6. **maintenance_requests** - Maintenance request records

## 🔐 Authentication System

### Default Admin Account

On first run, a default admin account is created:

- **Username**: `admin`
- **Password**: `admin123`
- **Role**: `admin`

**⚠️ Important**: Change the default password in production!

### User Registration

New users can sign up with:
- Username (unique)
- Email (unique)
- Password (minimum 6 characters)
- Full Name (optional)

### Login Features

- Session-based authentication
- Password hashing (SHA256)
- User roles (admin, user)
- Account status (active/inactive)

## 🚀 How to Use

### First Time Setup

1. **Start the web server**:
   ```bash
   python web_app.py
   ```

2. **Database is created automatically**:
   - File: `gearguard.db` in project root
   - Tables created on first run
   - Default admin user created

3. **Login with default credentials**:
   - Go to: http://127.0.0.1:5000/login
   - Username: `admin`
   - Password: `admin123`

### Creating New Users

1. Click **"Sign Up"** in navigation
2. Fill in the registration form
3. Login with new credentials

### Protected Routes

All main routes are now protected:
- Dashboard
- Equipment Management
- Maintenance Requests
- Teams
- Calendar

Users must login to access these pages.

## 📁 Database File

- **Location**: `gearguard.db` (in project root)
- **Backup**: Copy this file to backup your data
- **Reset**: Delete the file to start fresh (will recreate on next run)

## 🔧 Database Management

### View Database

You can use SQLite browser tools:
- **DB Browser for SQLite** (free, GUI)
- **SQLite CLI**: `sqlite3 gearguard.db`

### Backup Database

```bash
# Copy the database file
cp gearguard.db gearguard_backup.db
```

### Reset Database

```bash
# Delete and restart (will recreate)
rm gearguard.db
python web_app.py
```

## 🔒 Security Features

1. **Password Hashing**: SHA256 hashing (not plain text)
2. **Session Management**: Flask sessions with secret key
3. **Route Protection**: `@login_required` decorator
4. **Input Validation**: Form validation on signup/login

## 📝 User Roles

- **admin**: Full access (can be extended for admin features)
- **user**: Standard user access

## 🎨 UI Features

- Beautiful login/signup pages with gradient design
- User dropdown in navigation (when logged in)
- Flash messages for feedback
- Responsive design

## 🔄 Migration from In-Memory

The system still supports the original in-memory models for CLI usage (`app.py`, `demo.py`), but the web interface now uses the database.

## 🐛 Troubleshooting

**Database locked error?**
- Make sure only one instance of the app is running
- Close any database browser tools

**Can't login?**
- Check if database file exists
- Try resetting database (delete `gearguard.db`)
- Default credentials: admin/admin123

**Import errors?**
- Make sure `database.py` is in project root
- Check that `models/user.py` exists

## 📚 Next Steps

- Add password reset functionality
- Add user profile management
- Add role-based permissions
- Add audit logging
- Migrate to PostgreSQL for production

