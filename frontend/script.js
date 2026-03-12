document.addEventListener('DOMContentLoaded', () => {
    // Add scroll effect to navbar
    const navbar = document.querySelector('.navbar');
    
    window.addEventListener('scroll', () => {
        if (window.scrollY > 20) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // Form Submissions Intercept
    const signupForm = document.getElementById('signupForm');
    if (signupForm) {
        signupForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const btn = signupForm.querySelector('button');
            const originalText = btn.textContent;
            
            btn.textContent = 'Processing...';
            btn.style.opacity = '0.8';
            
            // Simulate API call
            setTimeout(() => {
                btn.textContent = 'Account Created! 🎉';
                btn.style.backgroundColor = 'var(--success-color)';
                btn.style.boxShadow = '0 10px 30px -10px rgba(16, 185, 129, 0.4)';
                
                setTimeout(() => {
                    signupForm.reset();
                    btn.textContent = originalText;
                    btn.style.backgroundColor = '';
                    btn.style.boxShadow = '';
                }, 3000);
            }, 1000);
        });
    }

    const subscribeForm = document.getElementById('subscribeForm');
    if (subscribeForm) {
        subscribeForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const btn = subscribeForm.querySelector('button');
            const originalText = btn.textContent;
            
            btn.textContent = 'Subscribing...';
            
            // Simulate API call
            setTimeout(() => {
                btn.textContent = 'Subscribed! ✨';
                btn.style.backgroundColor = 'var(--success-color)';
                
                setTimeout(() => {
                    subscribeForm.reset();
                    btn.textContent = originalText;
                    btn.style.backgroundColor = '';
                }, 3000);
            }, 1000);
        });
    }

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Modal Logic
    const loginBtn = document.getElementById('loginBtn');
    const loginModal = document.getElementById('loginModal');
    const closeModal = document.getElementById('closeModal');
    
    if (loginBtn && loginModal && closeModal) {
        loginBtn.addEventListener('click', (e) => {
            e.preventDefault();
            loginModal.classList.add('active');
            document.body.style.overflow = 'hidden'; 
        });

        closeModal.addEventListener('click', () => {
            loginModal.classList.remove('active');
            document.body.style.overflow = '';
        });

        loginModal.addEventListener('click', (e) => {
            if (e.target === loginModal) {
                loginModal.classList.remove('active');
                document.body.style.overflow = '';
            }
        });
    }

    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const btn = loginForm.querySelector('button');
            const originalText = btn.textContent;
            
            btn.textContent = 'Logging in...';
            btn.style.opacity = '0.8';
            
            setTimeout(() => {
                btn.textContent = 'Success! ✨';
                btn.style.backgroundColor = 'var(--success-color)';
                btn.style.boxShadow = '0 10px 30px -10px rgba(16, 185, 129, 0.4)';
                
                setTimeout(() => {
                    window.location.href = 'patient-dashboard.html';
                }, 1500);
            }, 1000);
        });
    }
});
