document.addEventListener('DOMContentLoaded', () => {
    // Tab Switching Logic
    const navItems = document.querySelectorAll('.sidebar-nav .nav-item[data-target]');
    const viewSections = document.querySelectorAll('.view-section');

    navItems.forEach(item => {
        item.addEventListener('click', () => {
            // Remove active class from all nav items
            navItems.forEach(nav => nav.classList.remove('active'));
            // Add active class to clicked nav item
            item.classList.add('active');

            // Hide all sections
            viewSections.forEach(section => section.classList.remove('active'));
            
            // Show target section
            const targetId = item.getAttribute('data-target');
            document.getElementById(targetId).classList.add('active');
        });
    });

    // Doctor Selection Logic
    const docCards = document.querySelectorAll('.doctor-list .doc-card');
    docCards.forEach(card => {
        card.addEventListener('click', () => {
            // Remove selected from siblings in the same list
            const siblings = card.parentElement.querySelectorAll('.doc-card');
            siblings.forEach(sib => sib.classList.remove('selected'));
            
            card.classList.add('selected');
        });
    });

    // File Upload Display Name
    const fileInput = document.getElementById('medicalFile');
    const fileNameDisplay = document.getElementById('fileNameDisplay');
    
    if (fileInput && fileNameDisplay) {
        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                fileNameDisplay.textContent = e.target.files[0].name;
                fileNameDisplay.style.color = 'var(--primary-color)';
                fileNameDisplay.style.fontWeight = '600';
            } else {
                fileNameDisplay.textContent = 'No file chosen (PDF, JPG, PNG)';
                fileNameDisplay.style.color = 'var(--text-muted)';
                fileNameDisplay.style.fontWeight = 'normal';
            }
        });
    }

    // Voice Agent Interaction Simulator
    const voiceBtn = document.getElementById('voiceAgentBtn');
    if (voiceBtn) {
        let isRecording = false;
        voiceBtn.addEventListener('click', () => {
            isRecording = !isRecording;
            if (isRecording) {
                voiceBtn.classList.add('recording');
                voiceBtn.textContent = '⏹️';
                // Find textarea and visually show it's listening
                const textarea = document.querySelector('.input-options textarea');
                if(textarea) {
                    textarea.placeholder = "Listening... Speak now...";
                }
            } else {
                voiceBtn.classList.remove('recording');
                voiceBtn.textContent = '🎙️';
                const textarea = document.querySelector('.input-options textarea');
                if(textarea) {
                    textarea.value = "I have been experiencing a mild fever and continuous headache for the past 2 days. I also have a sore throat.";
                    textarea.placeholder = "Type your symptoms, duration, and any previous medications here...";
                }
            }
        });
    }

    // Edit Profile Stub
    const editBtn = document.getElementById('editProfileBtn');
    if (editBtn) {
        editBtn.addEventListener('click', () => {
            alert('Edit Profile modal would open here.');
        });
    }
});
