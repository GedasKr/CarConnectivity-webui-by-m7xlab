/**
 * Main JavaScript for CarConnectivity WebUI
 * Handles core functionality and interactions
 */

(function() {
  'use strict';

  // ============================================
  // Initialize on DOM ready
  // ============================================
  
  document.addEventListener('DOMContentLoaded', function() {
    initTheme();
    initNavigation();
    initTabs();
    initTimeConversion();
    initTooltips();
    initScrollReveal();
    initMobileMenu();
  });

  // ============================================
  // Theme Management
  // ============================================
  
  function initTheme() {
    // Load saved theme or detect system preference
    const savedTheme = localStorage.getItem('theme');
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const theme = savedTheme || (systemPrefersDark ? 'dark' : 'light');
    
    setTheme(theme);
    
    // Listen for theme toggle clicks
    const themeToggles = document.querySelectorAll('.theme-toggle');
    themeToggles.forEach(toggle => {
      toggle.addEventListener('click', toggleTheme);
    });
    
    // Listen for system theme changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
      if (!localStorage.getItem('theme')) {
        setTheme(e.matches ? 'dark' : 'light');
      }
    });
  }
  
  function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
    
    // Update theme toggle icon if exists
    const themeToggles = document.querySelectorAll('.theme-toggle');
    themeToggles.forEach(toggle => {
      const icon = toggle.querySelector('.theme-icon');
      if (icon) {
        icon.textContent = theme === 'dark' ? '☀️' : '🌙';
      }
    });
  }
  
  function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    setTheme(newTheme);
  }

  // ============================================
  // Navigation
  // ============================================
  
  function initNavigation() {
    // Handle dropdown hover/click
    const dropdowns = document.querySelectorAll('.dropdown');
    dropdowns.forEach(dropdown => {
      const menu = dropdown.querySelector('.dropdown-menu');
      if (!menu) return;
      
      // Desktop: hover
      if (window.innerWidth >= 768) {
        dropdown.addEventListener('mouseenter', () => {
          menu.style.display = 'block';
          setTimeout(() => {
            menu.classList.add('show');
          }, 10);
        });
        
        dropdown.addEventListener('mouseleave', () => {
          menu.classList.remove('show');
          setTimeout(() => {
            if (!menu.classList.contains('show')) {
              menu.style.display = 'none';
            }
          }, 300);
        });
      }
      // Mobile: click
      else {
        const toggle = dropdown.querySelector('.nav-link');
        if (toggle) {
          toggle.addEventListener('click', (e) => {
            e.preventDefault();
            menu.classList.toggle('show');
          });
        }
      }
    });
  }

  // ============================================
  // Mobile Menu
  // ============================================
  
  function initMobileMenu() {
    const toggler = document.querySelector('.navbar-toggler');
    const nav = document.querySelector('.navbar-nav');
    
    if (toggler && nav) {
      toggler.addEventListener('click', () => {
        nav.classList.toggle('active');
        toggler.classList.toggle('active');
      });
      
      // Close menu when clicking outside
      document.addEventListener('click', (e) => {
        if (!toggler.contains(e.target) && !nav.contains(e.target)) {
          nav.classList.remove('active');
          toggler.classList.remove('active');
        }
      });
    }
  }

  // ============================================
  // Tabs
  // ============================================
  
  function initTabs() {
    const tabLinks = document.querySelectorAll('[data-bs-toggle="tab"]');
    
    tabLinks.forEach(link => {
      link.addEventListener('click', function(e) {
        e.preventDefault();
        
        const targetId = this.getAttribute('href');
        const targetPane = document.querySelector(targetId);
        
        if (!targetPane) return;
        
        // Remove active from all tabs and panes
        const allLinks = this.closest('.nav-tabs').querySelectorAll('.nav-link');
        const allPanes = document.querySelectorAll('.tab-pane');
        
        allLinks.forEach(l => l.classList.remove('active'));
        allPanes.forEach(p => p.classList.remove('active'));
        
        // Add active to clicked tab and target pane
        this.classList.add('active');
        targetPane.classList.add('active');
      });
    });
  }

  // ============================================
  // Time Conversion
  // ============================================
  
  function initTimeConversion() {
    // Convert ISO timestamps to local time
    const timeElements = document.querySelectorAll('.js-convert-time');
    timeElements.forEach(element => {
      const isoTime = element.textContent.trim();
      try {
        const date = new Date(isoTime);
        element.textContent = date.toLocaleString();
      } catch (e) {
        console.error('Failed to parse time:', isoTime);
      }
    });
    
    // Convert timestamps in tooltips
    const tooltipElements = document.querySelectorAll('.js-convert-time-title');
    tooltipElements.forEach(element => {
      const title = element.getAttribute('title');
      if (title) {
        const converted = title.replace(/\$\$\$([\s0-9:\+\.\-TZ]+)\$\$\$/g, (match, p1) => {
          try {
            return new Date(p1).toLocaleString();
          } catch (e) {
            return p1;
          }
        });
        element.setAttribute('title', converted);
      }
    });
  }

  // ============================================
  // Tooltips
  // ============================================
  
  function initTooltips() {
    const tooltipElements = document.querySelectorAll('[data-toggle="tooltip"]');
    
    tooltipElements.forEach(element => {
      element.addEventListener('mouseenter', function() {
        showTooltip(this);
      });
      
      element.addEventListener('mouseleave', function() {
        hideTooltip(this);
      });
    });
  }
  
  function showTooltip(element) {
    const title = element.getAttribute('title');
    if (!title) return;
    
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip-popup';
    tooltip.textContent = title;
    tooltip.style.whiteSpace = 'pre-line';
    
    document.body.appendChild(tooltip);
    
    const rect = element.getBoundingClientRect();
    tooltip.style.position = 'absolute';
    tooltip.style.top = (rect.top - tooltip.offsetHeight - 8) + 'px';
    tooltip.style.left = (rect.left + rect.width / 2 - tooltip.offsetWidth / 2) + 'px';
    tooltip.style.background = 'var(--color-surface-elevated)';
    tooltip.style.padding = 'var(--space-sm) var(--space-md)';
    tooltip.style.borderRadius = 'var(--border-radius-sm)';
    tooltip.style.boxShadow = 'var(--shadow-lg)';
    tooltip.style.fontSize = 'var(--font-size-sm)';
    tooltip.style.zIndex = '9999';
    tooltip.style.pointerEvents = 'none';
    
    element._tooltip = tooltip;
  }
  
  function hideTooltip(element) {
    if (element._tooltip) {
      element._tooltip.remove();
      delete element._tooltip;
    }
  }

  // ============================================
  // Scroll Reveal
  // ============================================
  
  function initScrollReveal() {
    const revealElements = document.querySelectorAll('.scroll-reveal');
    
    if (revealElements.length === 0) return;
    
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('revealed');
        }
      });
    }, {
      threshold: 0.1,
      rootMargin: '0px 0px -50px 0px'
    });
    
    revealElements.forEach(element => {
      observer.observe(element);
    });
  }

  // ============================================
  // Clickable Rows
  // ============================================
  
  document.addEventListener('click', function(e) {
    const clickableRow = e.target.closest('[data-href]');
    if (clickableRow) {
      const href = clickableRow.getAttribute('data-href');
      if (href) {
        window.location.href = href;
      }
    }
  });

  // ============================================
  // Alert Dismissal
  // ============================================
  
  document.addEventListener('click', function(e) {
    if (e.target.classList.contains('btn-close')) {
      const alert = e.target.closest('.alert');
      if (alert) {
        alert.style.animation = 'fadeOut 0.3s ease';
        setTimeout(() => {
          alert.remove();
        }, 300);
      }
    }
  });

  // ============================================
  // Form Enhancements
  // ============================================
  
  // Auto-focus first input in forms
  const forms = document.querySelectorAll('form');
  forms.forEach(form => {
    const firstInput = form.querySelector('input:not([type="hidden"]):not([type="submit"])');
    if (firstInput && !form.hasAttribute('data-no-autofocus')) {
      firstInput.focus();
    }
  });

  // ============================================
  // Utility Functions
  // ============================================
  
  window.CarConnectivity = {
    setTheme: setTheme,
    toggleTheme: toggleTheme,
    showTooltip: showTooltip,
    hideTooltip: hideTooltip
  };

})();
