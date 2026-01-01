// Mobile Navigation Toggle
const navbarToggle = document.getElementById('navbarToggle');
const navbarLinks = document.getElementById('navbarLinks');

if (navbarToggle) {
    navbarToggle.addEventListener('click', () => {
        navbarLinks.classList.toggle('active');
    });
}

// Mock Lab Tests Data
const mockTests = [
    {
        id: 1,
        name: "Complete Blood Count (CBC)",
        category: "blood",
        icon: "🩸",
        price: 25,
        fasting: false,
        duration: "24 hours",
        description: "Measures various components of blood including red blood cells, white blood cells, hemoglobin, and platelets.",
        parameters: ["Hemoglobin", "RBC", "WBC", "Platelets", "Hematocrit"],
        preparation: [
            "No special preparation required",
            "Can be done at any time of the day",
            "Inform your doctor about any medications"
        ],
        commonFor: ["Anemia", "Infection", "Blood disorders", "Overall health check"]
    },
    {
        id: 2,
        name: "Lipid Profile",
        category: "blood",
        icon: "💉",
        price: 35,
        fasting: true,
        duration: "24 hours",
        description: "Evaluates cholesterol levels and assesses the risk of cardiovascular diseases.",
        parameters: ["Total Cholesterol", "LDL", "HDL", "Triglycerides", "VLDL"],
        preparation: [
            "Fasting for 12-14 hours required",
            "Only water is allowed during fasting",
            "Avoid alcohol 24 hours before test",
            "Continue regular medications unless advised otherwise"
        ],
        commonFor: ["Heart disease risk", "High cholesterol", "Diabetes management", "Health screening"]
    },
    {
        id: 3,
        name: "Blood Sugar (Fasting)",
        category: "diabetes",
        icon: "🍬",
        price: 15,
        fasting: true,
        duration: "Same day",
        description: "Measures blood glucose levels after fasting to screen for diabetes and prediabetes.",
        parameters: ["Glucose"],
        preparation: [
            "Fasting for 8-12 hours required",
            "Drink only water during fasting period",
            "Take morning medications after the test",
            "Schedule early morning appointment"
        ],
        commonFor: ["Diabetes screening", "Prediabetes", "Blood sugar monitoring", "Health checkup"]
    },
    {
        id: 4,
        name: "HbA1c (Glycated Hemoglobin)",
        category: "diabetes",
        icon: "📊",
        price: 45,
        fasting: false,
        duration: "24 hours",
        description: "Measures average blood sugar levels over the past 2-3 months for diabetes management.",
        parameters: ["HbA1c percentage"],
        preparation: [
            "No fasting required",
            "Can be done at any time",
            "Continue regular diet and medications"
        ],
        commonFor: ["Diabetes diagnosis", "Long-term glucose control", "Treatment monitoring"]
    },
    {
        id: 5,
        name: "Thyroid Profile (TSH, T3, T4)",
        category: "thyroid",
        icon: "🦋",
        price: 65,
        fasting: false,
        duration: "24-48 hours",
        description: "Evaluates thyroid function and helps diagnose thyroid disorders.",
        parameters: ["TSH", "T3", "T4", "Free T3", "Free T4"],
        preparation: [
            "No fasting required",
            "Best done in the morning",
            "Inform about thyroid medications",
            "Avoid biotin supplements 2 days before"
        ],
        commonFor: ["Thyroid disorders", "Weight changes", "Fatigue", "Metabolism issues"]
    },
    {
        id: 6,
        name: "Liver Function Test (LFT)",
        category: "liver",
        icon: "🫀",
        price: 55,
        fasting: true,
        duration: "24 hours",
        description: "Assesses liver health and detects liver diseases through enzyme and protein levels.",
        parameters: ["ALT", "AST", "ALP", "Bilirubin", "Albumin", "Total Protein"],
        preparation: [
            "Fasting for 8-12 hours recommended",
            "Avoid alcohol 24 hours before",
            "Inform about medications and supplements",
            "Stay well hydrated"
        ],
        commonFor: ["Liver disease", "Hepatitis", "Jaundice", "Medication monitoring"]
    },
    {
        id: 7,
        name: "Kidney Function Test (KFT)",
        category: "kidney",
        icon: "🫘",
        price: 50,
        fasting: false,
        duration: "24 hours",
        description: "Evaluates kidney function through blood and urine tests.",
        parameters: ["Creatinine", "BUN", "Uric Acid", "Electrolytes", "GFR"],
        preparation: [
            "No fasting required",
            "Adequate water intake before test",
            "Avoid vigorous exercise 24 hours before",
            "List all current medications"
        ],
        commonFor: ["Kidney disease", "High blood pressure", "Diabetes", "Urinary problems"]
    },
    {
        id: 8,
        name: "Vitamin D (25-Hydroxy)",
        category: "blood",
        icon: "☀️",
        price: 70,
        fasting: false,
        duration: "2-3 days",
        description: "Measures vitamin D levels to assess bone health and immune function.",
        parameters: ["25-OH Vitamin D"],
        preparation: [
            "No fasting required",
            "Can be done at any time",
            "Inform about vitamin supplements"
        ],
        commonFor: ["Vitamin D deficiency", "Bone health", "Fatigue", "Weak immunity"]
    },
    {
        id: 9,
        name: "Vitamin B12",
        category: "blood",
        icon: "💊",
        price: 60,
        fasting: false,
        duration: "2-3 days",
        description: "Measures vitamin B12 levels essential for nerve function and blood cell production.",
        parameters: ["Cobalamin (B12)"],
        preparation: [
            "No fasting required",
            "Avoid B12 supplements 2 days before",
            "Inform about dietary habits"
        ],
        commonFor: ["Anemia", "Neurological symptoms", "Fatigue", "Vegetarian diet"]
    },
    {
        id: 10,
        name: "Electrocardiogram (ECG)",
        category: "cardiac",
        icon: "💓",
        price: 40,
        fasting: false,
        duration: "Same day",
        description: "Records electrical activity of the heart to detect heart problems.",
        parameters: ["Heart rhythm", "Heart rate", "Electrical conduction"],
        preparation: [
            "No fasting required",
            "Wear comfortable clothing",
            "Avoid caffeine 2 hours before",
            "Relax before the test"
        ],
        commonFor: ["Heart palpitations", "Chest pain", "Pre-surgery clearance", "Heart disease"]
    },
    {
        id: 11,
        name: "Chest X-Ray",
        category: "imaging",
        icon: "🫁",
        price: 80,
        fasting: false,
        duration: "Same day",
        description: "Imaging test to examine the lungs, heart, and chest wall.",
        parameters: ["Lung fields", "Heart size", "Bone structure"],
        preparation: [
            "No fasting required",
            "Remove jewelry and metal objects",
            "Inform if pregnant",
            "Wear loose clothing"
        ],
        commonFor: ["Respiratory problems", "Heart enlargement", "Lung infections", "Pre-employment"]
    },
    {
        id: 12,
        name: "Urine Routine Analysis",
        category: "blood",
        icon: "🧪",
        price: 20,
        fasting: false,
        duration: "Same day",
        description: "Examines urine for signs of kidney disease, urinary tract infections, and diabetes.",
        parameters: ["pH", "Protein", "Glucose", "Blood cells", "Bacteria"],
        preparation: [
            "Collect mid-stream urine sample",
            "Use clean container provided",
            "Preferably first morning sample",
            "Avoid contamination"
        ],
        commonFor: ["UTI", "Kidney problems", "Diabetes", "Health screening"]
    },
    {
        id: 13,
        name: "Iron Studies",
        category: "blood",
        icon: "🔩",
        price: 85,
        fasting: true,
        duration: "24-48 hours",
        description: "Comprehensive test to evaluate iron levels and iron storage in the body.",
        parameters: ["Serum Iron", "TIBC", "Ferritin", "Transferrin Saturation"],
        preparation: [
            "Fasting for 8-12 hours recommended",
            "Avoid iron supplements 24 hours before",
            "Best done in the morning",
            "Inform about menstrual cycle"
        ],
        commonFor: ["Anemia", "Iron deficiency", "Fatigue", "Heavy menstruation"]
    },
    {
        id: 14,
        name: "Prostate-Specific Antigen (PSA)",
        category: "blood",
        icon: "🎗️",
        price: 75,
        fasting: false,
        duration: "24 hours",
        description: "Screening test for prostate cancer and prostate health in men.",
        parameters: ["Total PSA", "Free PSA"],
        preparation: [
            "No fasting required",
            "Avoid ejaculation 48 hours before",
            "No vigorous exercise 24 hours before",
            "Avoid bike riding before test"
        ],
        commonFor: ["Prostate cancer screening", "Prostate enlargement", "Urinary symptoms", "Age 50+ men"]
    },
    {
        id: 15,
        name: "CA-125 (Cancer Marker)",
        category: "blood",
        icon: "🎗️",
        price: 90,
        fasting: false,
        duration: "2-3 days",
        description: "Tumor marker test primarily used for ovarian cancer screening and monitoring.",
        parameters: ["CA-125 level"],
        preparation: [
            "No fasting required",
            "Inform about menstrual cycle",
            "Mention any pelvic conditions",
            "List current medications"
        ],
        commonFor: ["Ovarian cancer screening", "Pelvic mass", "Treatment monitoring"]
    }
];

// State Management
let tests = [...mockTests];
let filteredTests = [...mockTests];
let currentCategory = 'all';
let currentView = 'card';

// DOM Elements
const searchInput = document.getElementById('searchInput');
const priceFilter = document.getElementById('priceFilter');
const fastingFilter = document.getElementById('fastingFilter');
const applyFiltersBtn = document.getElementById('applyFiltersBtn');
const resetFiltersBtn = document.getElementById('resetFiltersBtn');
const resultsCount = document.getElementById('resultsCount');
const testsGrid = document.getElementById('testsGrid');
const tableView = document.getElementById('tableView');
const testsTableBody = document.getElementById('testsTableBody');
const cardViewBtn = document.getElementById('cardViewBtn');
const tableViewBtn = document.getElementById('tableViewBtn');
const testDetailModal = document.getElementById('testDetailModal');
const closeModalBtn = document.getElementById('closeModalBtn');
const modalBody = document.getElementById('modalBody');

// Initialize
function init() {
    const urlParams = new URLSearchParams(window.location.search);
    const query = urlParams.get('q');
    if (query) {
        searchInput.value = query;
    }

    renderTests();
    attachEventListeners();
}

// Render Tests
function renderTests() {
    if (currentView === 'card') {
        renderCardView();
        testsGrid.style.display = 'grid';
        tableView.classList.remove('active');
    } else {
        renderTableView();
        testsGrid.style.display = 'none';
        tableView.classList.add('active');
    }
    updateResultsCount();
}

// Render Card View
function renderCardView() {
    if (filteredTests.length === 0) {
        testsGrid.innerHTML = `
            <div style="grid-column: 1/-1; text-align: center; padding: 3rem;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">😞</div>
                <h3>No tests found</h3>
                <p style="color: var(--text-muted);">Try adjusting your filters</p>
            </div>
        `;
        return;
    }

    testsGrid.innerHTML = filteredTests.map(test => createTestCard(test)).join('');
}

// Create Test Card
function createTestCard(test) {
    return `
        <div class="test-card">
            <div class="test-header">
                <div>
                    <div class="test-icon">${test.icon}</div>
                    <h3 class="test-name">${test.name}</h3>
                    <div class="test-category">${test.category}</div>
                </div>
                <div class="price-badge">
                    <span class="price-label">Starting at</span>
                    $${test.price}
                </div>
            </div>

            <p class="test-description">${test.description}</p>

            <div class="test-details">
                <div class="detail-row">
                    <span class="detail-icon">⏱️</span>
                    <span class="detail-label">Results:</span>
                    <span class="detail-value">${test.duration}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-icon">🍽️</span>
                    <span class="detail-label">Fasting:</span>
                    <span class="detail-value">${test.fasting ? 'Required (8-12 hours)' : 'Not Required'}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-icon">📋</span>
                    <span class="detail-label">Parameters:</span>
                    <span class="detail-value">${test.parameters.length} measured</span>
                </div>
            </div>

            <div class="parameters-list">
                ${test.parameters.slice(0, 3).map(param =>
                    `<span class="parameter-tag">${param}</span>`
                ).join('')}
                ${test.parameters.length > 3 ?
                    `<span class="parameter-tag">+${test.parameters.length - 3} more</span>` : ''}
            </div>

            <div class="test-actions">
                <button class="btn btn-primary btn-block" onclick="showTestDetails(${test.id})">
                    View Details
                </button>
            </div>
        </div>
    `;
}

// Render Table View
function renderTableView() {
    if (filteredTests.length === 0) {
        testsTableBody.innerHTML = `
            <tr>
                <td colspan="6" style="text-align: center; padding: 3rem;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">😞</div>
                    <h3>No tests found</h3>
                    <p style="color: var(--text-muted);">Try adjusting your filters</p>
                </td>
            </tr>
        `;
        return;
    }

    testsTableBody.innerHTML = filteredTests.map(test => `
        <tr>
            <td>
                <strong>${test.name}</strong><br>
                <small style="color: var(--text-muted);">${test.parameters.length} parameters</small>
            </td>
            <td><span class="badge badge-info">${test.category}</span></td>
            <td><strong style="color: var(--primary-teal);">$${test.price}</strong></td>
            <td>${test.fasting ? '✓ Required' : '✗ Not Required'}</td>
            <td>${test.duration}</td>
            <td>
                <button class="btn btn-sm btn-primary" onclick="showTestDetails(${test.id})">
                    View Details
                </button>
            </td>
        </tr>
    `).join('');
}

// Update Results Count
function updateResultsCount() {
    resultsCount.textContent = `${filteredTests.length} test${filteredTests.length !== 1 ? 's' : ''} found`;
}

// Apply Filters
function applyFilters() {
    const searchTerm = searchInput.value.toLowerCase();
    const maxPrice = parseFloat(priceFilter.value) || Infinity;
    const fastingReq = fastingFilter.value;

    filteredTests = tests.filter(test => {
        // Category filter
        const matchesCategory = currentCategory === 'all' || test.category === currentCategory;

        // Search filter
        const matchesSearch = !searchTerm ||
            test.name.toLowerCase().includes(searchTerm) ||
            test.description.toLowerCase().includes(searchTerm) ||
            test.parameters.some(p => p.toLowerCase().includes(searchTerm));

        // Price filter
        const matchesPrice = test.price <= maxPrice;

        // Fasting filter
        let matchesFasting = true;
        if (fastingReq === 'yes') matchesFasting = test.fasting;
        else if (fastingReq === 'no') matchesFasting = !test.fasting;

        return matchesCategory && matchesSearch && matchesPrice && matchesFasting;
    });

    renderTests();
}

// Reset Filters
function resetFilters() {
    searchInput.value = '';
    priceFilter.value = '';
    fastingFilter.value = '';
    currentCategory = 'all';

    // Reset category tabs
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.category === 'all') {
            btn.classList.add('active');
        }
    });

    filteredTests = [...tests];
    renderTests();
}

// Toggle View
function toggleView(view) {
    currentView = view;

    if (view === 'card') {
        cardViewBtn.classList.add('active');
        tableViewBtn.classList.remove('active');
    } else {
        cardViewBtn.classList.remove('active');
        tableViewBtn.classList.add('active');
    }

    renderTests();
}

// Show Test Details
window.showTestDetails = function(testId) {
    const test = tests.find(t => t.id === testId);
    if (!test) return;

    document.getElementById('modalTitle').textContent = test.name;

    modalBody.innerHTML = `
        <div class="modal-section">
            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 2rem;">
                <div>
                    <div style="font-size: 3rem; margin-bottom: 1rem;">${test.icon}</div>
                    <h3 style="font-size: 1.5rem; margin-bottom: 0.5rem;">${test.name}</h3>
                    <p style="color: var(--text-muted); text-transform: uppercase; font-size: 0.9rem;">${test.category} Test</p>
                </div>
                <div class="price-badge">
                    <span class="price-label">Price</span>
                    $${test.price}
                </div>
            </div>

            <p style="line-height: 1.8; color: var(--text-secondary); margin-bottom: 2rem;">
                ${test.description}
            </p>
        </div>

        <div class="modal-section">
            <h4 class="modal-section-title">📊 Parameters Measured (${test.parameters.length})</h4>
            <div class="parameters-list">
                ${test.parameters.map(param =>
                    `<span class="parameter-tag">${param}</span>`
                ).join('')}
            </div>
        </div>

        <div class="modal-section">
            <h4 class="modal-section-title">📋 Preparation Guidelines</h4>
            <ul class="preparation-list">
                ${test.preparation.map(item => `<li>${item}</li>`).join('')}
            </ul>
        </div>

        <div class="modal-section">
            <h4 class="modal-section-title">🏥 Commonly Used For</h4>
            <ul class="info-list">
                ${test.commonFor.map(item => `<li>${item}</li>`).join('')}
            </ul>
        </div>

        <div class="modal-section">
            <h4 class="modal-section-title">ℹ️ Additional Information</h4>
            <div class="detail-row" style="margin-bottom: 1rem;">
                <span class="detail-icon">⏱️</span>
                <span class="detail-label">Results Available:</span>
                <span class="detail-value">${test.duration}</span>
            </div>
            <div class="detail-row" style="margin-bottom: 1rem;">
                <span class="detail-icon">🍽️</span>
                <span class="detail-label">Fasting Required:</span>
                <span class="detail-value">${test.fasting ? 'Yes (8-12 hours)' : 'No'}</span>
            </div>
            <div class="detail-row">
                <span class="detail-icon">📍</span>
                <span class="detail-label">Sample Type:</span>
                <span class="detail-value">${test.category === 'imaging' ? 'Imaging scan' : test.category === 'cardiac' ? 'ECG test' : 'Blood sample'}</span>
            </div>
        </div>

        <div style="display: flex; gap: 1rem; margin-top: 2rem;">
            <button class="btn btn-primary btn-block" onclick="bookTest(${test.id})">
                Book This Test - $${test.price}
            </button>
            <button class="btn btn-outline" onclick="closeTestModal()">
                Close
            </button>
        </div>
    `;

    testDetailModal.classList.add('active');
};

// Book Test
window.bookTest = function(testId) {
    const test = tests.find(t => t.id === testId);
    alert(`Booking ${test.name}...\n\nIn a full implementation, this would:\n1. Show available time slots\n2. Collect patient information\n3. Process payment\n4. Send confirmation email\n\nPrice: $${test.price}`);
};

// Close Modal
window.closeTestModal = function() {
    testDetailModal.classList.remove('active');
};

// Event Listeners
function attachEventListeners() {
    // Filters
    applyFiltersBtn.addEventListener('click', applyFilters);
    resetFiltersBtn.addEventListener('click', resetFilters);
    searchInput.addEventListener('keyup', (e) => {
        if (e.key === 'Enter') applyFilters();
    });

    // View toggle
    cardViewBtn.addEventListener('click', () => toggleView('card'));
    tableViewBtn.addEventListener('click', () => toggleView('table'));

    // Category tabs
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentCategory = btn.dataset.category;
            applyFilters();
        });
    });

    // Modal
    closeModalBtn.addEventListener('click', closeTestModal);
    testDetailModal.addEventListener('click', (e) => {
        if (e.target === testDetailModal) closeTestModal();
    });
}

// Initialize on page load
window.addEventListener('load', init);
