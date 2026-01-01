// Mobile Navigation Toggle
const navbarToggle = document.getElementById('navbarToggle');
const navbarLinks = document.getElementById('navbarLinks');

if (navbarToggle) {
    navbarToggle.addEventListener('click', () => {
        navbarLinks.classList.toggle('active');
    });
}

// Mock Doctor Data
const mockDoctors = [
    {
        id: 1,
        name: "Dr. Sarah Johnson",
        specialty: "Cardiology",
        hospital: "NewYork-Presbyterian Hospital",
        location: "Manhattan",
        rating: 4.9,
        reviews: 156,
        experience: 15,
        patients: "2,500+",
        languages: ["English", "Spanish"],
        education: "MD, Harvard Medical School",
        consultationFee: 250,
        available: true
    },
    {
        id: 2,
        name: "Dr. Michael Chen",
        specialty: "Neurology",
        hospital: "Mount Sinai Hospital",
        location: "Manhattan",
        rating: 4.8,
        reviews: 142,
        experience: 12,
        patients: "1,800+",
        languages: ["English", "Mandarin"],
        education: "MD, Johns Hopkins University",
        consultationFee: 275,
        available: true
    },
    {
        id: 3,
        name: "Dr. Emily Rodriguez",
        specialty: "Pediatrics",
        hospital: "NYU Langone Health",
        location: "Manhattan",
        rating: 4.9,
        reviews: 198,
        experience: 10,
        patients: "3,200+",
        languages: ["English", "Spanish"],
        education: "MD, Columbia University",
        consultationFee: 200,
        available: true
    },
    {
        id: 4,
        name: "Dr. James Williams",
        specialty: "Orthopedics",
        hospital: "Lenox Hill Hospital",
        location: "Manhattan",
        rating: 4.7,
        reviews: 134,
        experience: 18,
        patients: "2,100+",
        languages: ["English"],
        education: "MD, Stanford University",
        consultationFee: 300,
        available: false
    },
    {
        id: 5,
        name: "Dr. Aisha Patel",
        specialty: "Dermatology",
        hospital: "Brooklyn Hospital Center",
        location: "Brooklyn",
        rating: 4.8,
        reviews: 167,
        experience: 8,
        patients: "1,600+",
        languages: ["English", "Hindi"],
        education: "MD, Yale School of Medicine",
        consultationFee: 225,
        available: true
    },
    {
        id: 6,
        name: "Dr. Robert Taylor",
        specialty: "Psychiatry",
        hospital: "Montefiore Medical Center",
        location: "Bronx",
        rating: 4.6,
        reviews: 89,
        experience: 20,
        patients: "1,200+",
        languages: ["English", "French"],
        education: "MD, Duke University",
        consultationFee: 280,
        available: true
    },
    {
        id: 7,
        name: "Dr. Lisa Zhang",
        specialty: "Oncology",
        hospital: "NYU Langone Health",
        location: "Manhattan",
        rating: 4.9,
        reviews: 203,
        experience: 14,
        patients: "1,900+",
        languages: ["English", "Mandarin"],
        education: "MD, University of Pennsylvania",
        consultationFee: 350,
        available: true
    },
    {
        id: 8,
        name: "Dr. David Kumar",
        specialty: "General Medicine",
        hospital: "Queens Hospital Center",
        location: "Queens",
        rating: 4.5,
        reviews: 112,
        experience: 7,
        patients: "2,800+",
        languages: ["English", "Hindi", "Tamil"],
        education: "MD, Boston University",
        consultationFee: 150,
        available: true
    }
];

// State Management
let doctors = [...mockDoctors];
let filteredDoctors = [...mockDoctors];
let selectedDoctor = null;
let selectedDate = null;
let selectedTime = null;
let currentStep = 1;
let currentMonth = new Date().getMonth();
let currentYear = new Date().getFullYear();

// DOM Elements
const searchInput = document.getElementById('searchInput');
const specialtyFilter = document.getElementById('specialtyFilter');
const locationFilter = document.getElementById('locationFilter');
const availabilityFilter = document.getElementById('availabilityFilter');
const applyFiltersBtn = document.getElementById('applyFiltersBtn');
const resetFiltersBtn = document.getElementById('resetFiltersBtn');
const resultsCount = document.getElementById('resultsCount');
const doctorsGrid = document.getElementById('doctorsGrid');
const bookingModal = document.getElementById('bookingModal');
const closeModalBtn = document.getElementById('closeModalBtn');
const backBtn = document.getElementById('backBtn');
const nextBtn = document.getElementById('nextBtn');

// Initialize
function init() {
    const urlParams = new URLSearchParams(window.location.search);
    const query = urlParams.get('q');
    if (query) {
        searchInput.value = query;
    }

    renderDoctors();
    attachEventListeners();
}

// Render Doctors
function renderDoctors() {
    if (filteredDoctors.length === 0) {
        doctorsGrid.innerHTML = `
            <div style="grid-column: 1/-1; text-align: center; padding: 3rem;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">😞</div>
                <h3>No doctors found</h3>
                <p style="color: var(--text-muted);">Try adjusting your filters</p>
            </div>
        `;
        resultsCount.textContent = '0 doctors found';
        return;
    }

    doctorsGrid.innerHTML = filteredDoctors.map(doctor => createDoctorCard(doctor)).join('');
    resultsCount.textContent = `${filteredDoctors.length} doctor${filteredDoctors.length !== 1 ? 's' : ''} found`;
}

// Create Doctor Card
function createDoctorCard(doctor) {
    const initials = doctor.name.split(' ').map(n => n[0]).join('');
    const availabilityBadge = doctor.available
        ? '<span class="availability-badge available">✅ Available This Week</span>'
        : '<span class="availability-badge busy">⏰ Fully Booked</span>';

    return `
        <div class="doctor-card">
            <div class="doctor-header">
                <div class="doctor-photo">${initials}</div>
                <div class="doctor-info">
                    <h3 class="doctor-name">${doctor.name}</h3>
                    <div class="doctor-specialty">${doctor.specialty}</div>
                    <div class="doctor-hospital">📍 ${doctor.hospital}</div>
                </div>
            </div>

            <div class="doctor-stats">
                <div class="stat-item">
                    <div class="stat-value">${doctor.experience}</div>
                    <div class="stat-label">Years Exp.</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">${doctor.patients}</div>
                    <div class="stat-label">Patients</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">$${doctor.consultationFee}</div>
                    <div class="stat-label">Fee</div>
                </div>
            </div>

            <div class="rating-display">
                <span class="stars">${'★'.repeat(Math.floor(doctor.rating))}${'☆'.repeat(5 - Math.floor(doctor.rating))}</span>
                <span class="rating-number">${doctor.rating}</span>
                <span class="rating-count">(${doctor.reviews} reviews)</span>
            </div>

            <div class="doctor-details">
                <div class="detail-row">
                    <span class="detail-icon">🎓</span>
                    ${doctor.education}
                </div>
                <div class="detail-row">
                    <span class="detail-icon">🗣️</span>
                    ${doctor.languages.join(', ')}
                </div>
            </div>

            ${availabilityBadge}

            <div class="doctor-actions">
                <button class="btn btn-primary btn-block" onclick="openBookingModal(${doctor.id})" ${!doctor.available ? 'disabled' : ''}>
                    ${doctor.available ? '📅 Book Appointment' : '🔒 Not Available'}
                </button>
            </div>
        </div>
    `;
}

// Apply Filters
function applyFilters() {
    const searchTerm = searchInput.value.toLowerCase();
    const specialty = specialtyFilter.value.toLowerCase();
    const location = locationFilter.value.toLowerCase();
    const availability = availabilityFilter.value;

    filteredDoctors = doctors.filter(doctor => {
        const matchesSearch = !searchTerm ||
            doctor.name.toLowerCase().includes(searchTerm) ||
            doctor.hospital.toLowerCase().includes(searchTerm);

        const matchesSpecialty = !specialty || doctor.specialty.toLowerCase() === specialty;
        const matchesLocation = !location || doctor.location.toLowerCase() === location;
        const matchesAvailability = !availability || doctor.available;

        return matchesSearch && matchesSpecialty && matchesLocation && matchesAvailability;
    });

    renderDoctors();
}

// Reset Filters
function resetFilters() {
    searchInput.value = '';
    specialtyFilter.value = '';
    locationFilter.value = '';
    availabilityFilter.value = '';
    filteredDoctors = [...doctors];
    renderDoctors();
}

// Open Booking Modal
window.openBookingModal = function(doctorId) {
    selectedDoctor = doctors.find(d => d.id === doctorId);
    if (!selectedDoctor) return;

    currentStep = 1;
    selectedDate = null;
    selectedTime = null;

    document.getElementById('modalTitle').textContent = `Book Appointment with ${selectedDoctor.name}`;
    bookingModal.classList.add('active');

    updateStepDisplay();
    renderCalendar();
};

// Close Modal
function closeModal() {
    bookingModal.classList.remove('active');
    resetBookingForm();
}

// Update Step Display
function updateStepDisplay() {
    // Update step indicators
    document.querySelectorAll('.step').forEach((step, index) => {
        const stepNum = index + 1;
        step.classList.remove('active', 'completed');

        if (stepNum < currentStep) {
            step.classList.add('completed');
        } else if (stepNum === currentStep) {
            step.classList.add('active');
        }
    });

    // Update sections
    document.querySelectorAll('.booking-section').forEach(section => {
        section.classList.remove('active');
    });
    document.querySelector(`[data-section="${currentStep}"]`).classList.add('active');

    // Update buttons
    backBtn.style.display = currentStep > 1 && currentStep < 4 ? 'block' : 'none';

    if (currentStep === 4) {
        nextBtn.style.display = 'none';
    } else {
        nextBtn.style.display = 'block';
        nextBtn.textContent = currentStep === 3 ? 'Confirm Appointment' : 'Next';
    }
}

// Calendar Rendering
function renderCalendar() {
    const calendarTitle = document.getElementById('calendarTitle');
    const calendarGrid = document.getElementById('calendarGrid');

    const monthNames = ['January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'];

    calendarTitle.textContent = `${monthNames[currentMonth]} ${currentYear}`;

    const firstDay = new Date(currentYear, currentMonth, 1).getDay();
    const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();
    const today = new Date();

    let html = '';

    // Weekday headers
    const weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    weekdays.forEach(day => {
        html += `<div class="weekday-header">${day}</div>`;
    });

    // Empty cells for days before month starts
    for (let i = 0; i < firstDay; i++) {
        html += '<div class="calendar-day disabled"></div>';
    }

    // Days of the month
    for (let day = 1; day <= daysInMonth; day++) {
        const date = new Date(currentYear, currentMonth, day);
        const isToday = date.toDateString() === today.toDateString();
        const isPast = date < today && !isToday;
        const isSelected = selectedDate && date.toDateString() === selectedDate.toDateString();

        let classes = 'calendar-day';
        if (isToday) classes += ' today';
        if (isPast) classes += ' disabled';
        if (isSelected) classes += ' selected';

        html += `<div class="${classes}" onclick="selectDate(${currentYear}, ${currentMonth}, ${day})" ${isPast ? 'style="pointer-events: none;"' : ''}>
            ${day}
        </div>`;
    }

    calendarGrid.innerHTML = html;
}

// Navigate Calendar
document.getElementById('prevMonth').addEventListener('click', () => {
    currentMonth--;
    if (currentMonth < 0) {
        currentMonth = 11;
        currentYear--;
    }
    renderCalendar();
});

document.getElementById('nextMonth').addEventListener('click', () => {
    currentMonth++;
    if (currentMonth > 11) {
        currentMonth = 0;
        currentYear++;
    }
    renderCalendar();
});

// Select Date
window.selectDate = function(year, month, day) {
    selectedDate = new Date(year, month, day);
    renderCalendar();
};

// Render Time Slots
function renderTimeSlots() {
    const morningSlots = document.getElementById('morningSlots');
    const afternoonSlots = document.getElementById('afternoonSlots');
    const eveningSlots = document.getElementById('eveningSlots');

    const dateText = selectedDate.toLocaleDateString('en-US', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
    document.getElementById('selectedDateText').textContent = dateText;

    // Morning slots (9 AM - 12 PM)
    const morningTimes = ['9:00 AM', '9:30 AM', '10:00 AM', '10:30 AM', '11:00 AM', '11:30 AM'];
    morningSlots.innerHTML = morningTimes.map(time => {
        const isBooked = Math.random() > 0.7; // Random booking simulation
        return `<div class="time-slot ${isBooked ? 'booked' : ''}" onclick="selectTime('${time}')">${time}</div>`;
    }).join('');

    // Afternoon slots (12 PM - 5 PM)
    const afternoonTimes = ['12:00 PM', '12:30 PM', '1:00 PM', '1:30 PM', '2:00 PM', '2:30 PM',
        '3:00 PM', '3:30 PM', '4:00 PM', '4:30 PM'];
    afternoonSlots.innerHTML = afternoonTimes.map(time => {
        const isBooked = Math.random() > 0.7;
        return `<div class="time-slot ${isBooked ? 'booked' : ''}" onclick="selectTime('${time}')">${time}</div>`;
    }).join('');

    // Evening slots (5 PM - 8 PM)
    const eveningTimes = ['5:00 PM', '5:30 PM', '6:00 PM', '6:30 PM', '7:00 PM', '7:30 PM'];
    eveningSlots.innerHTML = eveningTimes.map(time => {
        const isBooked = Math.random() > 0.7;
        return `<div class="time-slot ${isBooked ? 'booked' : ''}" onclick="selectTime('${time}')">${time}</div>`;
    }).join('');
}

// Select Time
window.selectTime = function(time) {
    // Remove previous selection
    document.querySelectorAll('.time-slot').forEach(slot => {
        slot.classList.remove('selected');
    });

    // Add selection to clicked slot if not booked
    const clickedSlot = Array.from(document.querySelectorAll('.time-slot'))
        .find(slot => slot.textContent === time && !slot.classList.contains('booked'));

    if (clickedSlot) {
        clickedSlot.classList.add('selected');
        selectedTime = time;
    }
};

// Update Summary
function updateSummary() {
    document.getElementById('summaryDoctor').textContent = selectedDoctor.name;
    document.getElementById('summaryDate').textContent = selectedDate.toLocaleDateString('en-US', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
    document.getElementById('summaryTime').textContent = selectedTime;
}

// Validate Step
function validateStep() {
    if (currentStep === 1) {
        if (!selectedDate) {
            alert('Please select a date for your appointment');
            return false;
        }
    } else if (currentStep === 2) {
        if (!selectedTime) {
            alert('Please select a time slot for your appointment');
            return false;
        }
    } else if (currentStep === 3) {
        const form = document.getElementById('patientForm');
        if (!form.checkValidity()) {
            form.reportValidity();
            return false;
        }
    }
    return true;
}

// Next Step
function nextStep() {
    if (!validateStep()) return;

    if (currentStep === 2) {
        updateSummary();
    }

    if (currentStep === 3) {
        confirmAppointment();
        return;
    }

    currentStep++;
    updateStepDisplay();

    if (currentStep === 2) {
        renderTimeSlots();
    }
}

// Previous Step
function previousStep() {
    if (currentStep > 1) {
        currentStep--;
        updateStepDisplay();
    }
}

// Confirm Appointment
function confirmAppointment() {
    const patientName = document.getElementById('patientName').value;
    const patientEmail = document.getElementById('patientEmail').value;
    const patientPhone = document.getElementById('patientPhone').value;

    // Generate confirmation ID
    const confirmationId = 'APT-' + Math.random().toString(36).substr(2, 9).toUpperCase();

    // Update confirmation details
    document.getElementById('confirmationId').textContent = confirmationId;
    document.getElementById('confirmDoctor').textContent = selectedDoctor.name;
    document.getElementById('confirmDateTime').textContent =
        selectedDate.toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' }) +
        ' at ' + selectedTime;
    document.getElementById('confirmPatient').textContent = patientName;
    document.getElementById('confirmContact').textContent = `${patientEmail} • ${patientPhone}`;

    currentStep = 4;
    updateStepDisplay();
}

// Reset Booking Form
function resetBookingForm() {
    currentStep = 1;
    selectedDate = null;
    selectedTime = null;
    document.getElementById('patientForm').reset();
}

// Event Listeners
function attachEventListeners() {
    applyFiltersBtn.addEventListener('click', applyFilters);
    resetFiltersBtn.addEventListener('click', resetFilters);
    searchInput.addEventListener('keyup', (e) => {
        if (e.key === 'Enter') applyFilters();
    });

    closeModalBtn.addEventListener('click', closeModal);
    bookingModal.addEventListener('click', (e) => {
        if (e.target === bookingModal) closeModal();
    });

    nextBtn.addEventListener('click', nextStep);
    backBtn.addEventListener('click', previousStep);
}

// Initialize on page load
window.addEventListener('load', init);
