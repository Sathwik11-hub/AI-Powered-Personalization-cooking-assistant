// Voice recognition functionality
let recognition;
let isListening = false;

function initializeVoiceRecognition() {
    if ('webkitSpeechRecognition' in window) {
        recognition = new webkitSpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';
        
        recognition.onstart = function() {
            isListening = true;
            console.log('Voice recognition started');
        };
        
        recognition.onresult = function(event) {
            const command = event.results[0][0].transcript;
            console.log('Voice command:', command);
            processVoiceCommand(command);
        };
        
        recognition.onerror = function(event) {
            console.error('Voice recognition error:', event.error);
            isListening = false;
        };
        
        recognition.onend = function() {
            isListening = false;
            console.log('Voice recognition ended');
        };
    } else {
        console.log('Voice recognition not supported');
    }
}

function startListening() {
    if (recognition && !isListening) {
        recognition.start();
    }
}

function stopListening() {
    if (recognition && isListening) {
        recognition.stop();
    }
}

function processVoiceCommand(command) {
    const commandLower = command.toLowerCase();
    
    // Recipe search commands
    if (commandLower.includes('find') || commandLower.includes('search')) {
        if (commandLower.includes('vegetarian')) {
            // Trigger vegetarian recipe search
            console.log('Searching for vegetarian recipes');
        } else if (commandLower.includes('chicken')) {
            // Trigger chicken recipe search
            console.log('Searching for chicken recipes');
        }
    }
    
    // Cooking mode commands
    if (commandLower.includes('next step')) {
        // Trigger next step in cooking mode
        console.log('Moving to next step');
    }
    
    if (commandLower.includes('repeat')) {
        // Repeat current step
        console.log('Repeating current step');
    }
    
    if (commandLower.includes('timer')) {
        // Set timer
        const timeMatch = commandLower.match(/(\d+)\s*(minute|hour)/);
        if (timeMatch) {
            const time = timeMatch[1];
            const unit = timeMatch[2];
            console.log(`Setting timer for ${time} ${unit}(s)`);
        }
    }
}

// Text-to-speech functionality
function speakText(text) {
    if ('speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 0.8;
        utterance.pitch = 1;
        utterance.volume = 0.8;
        speechSynthesis.speak(utterance);
    } else {
        console.log('Text-to-speech not supported');
    }
}

// Cooking timer functionality
let activeTimers = [];

function startTimer(minutes, name = 'Cooking Timer') {
    const timerObj = {
        id: Date.now(),
        name: name,
        duration: minutes * 60, // Convert to seconds
        remaining: minutes * 60,
        interval: null
    };
    
    timerObj.interval = setInterval(() => {
        timerObj.remaining--;
        
        if (timerObj.remaining <= 0) {
            clearInterval(timerObj.interval);
            notifyTimerComplete(timerObj);
            removeTimer(timerObj.id);
        }
        
        updateTimerDisplay(timerObj);
    }, 1000);
    
    activeTimers.push(timerObj);
    return timerObj.id;
}

function stopTimer(timerId) {
    const timer = activeTimers.find(t => t.id === timerId);
    if (timer) {
        clearInterval(timer.interval);
        removeTimer(timerId);
    }
}

function removeTimer(timerId) {
    activeTimers = activeTimers.filter(t => t.id !== timerId);
}

function updateTimerDisplay(timer) {
    const minutes = Math.floor(timer.remaining / 60);
    const seconds = timer.remaining % 60;
    const display = `${minutes}:${seconds.toString().padStart(2, '0')}`;
    console.log(`${timer.name}: ${display}`);
}

function notifyTimerComplete(timer) {
    // Visual notification
    console.log(`Timer "${timer.name}" completed!`);
    
    // Audio notification
    speakText(`${timer.name} is complete!`);
    
    // Browser notification (if permission granted)
    if (Notification.permission === 'granted') {
        new Notification('Cooking Timer', {
            body: `${timer.name} is complete!`,
            icon: '/static/images/timer-icon.png'
        });
    }
}

// Recipe scaling functionality
function scaleRecipe(originalServings, newServings, nutrition) {
    const scale = newServings / originalServings;
    const scaledNutrition = {};
    
    for (const [key, value] of Object.entries(nutrition)) {
        if (typeof value === 'number') {
            scaledNutrition[key] = Math.round(value * scale * 10) / 10;
        } else {
            scaledNutrition[key] = value;
        }
    }
    
    return scaledNutrition;
}

// Image processing helpers
function compressImage(file, maxWidth = 800, quality = 0.8) {
    return new Promise((resolve) => {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        const img = new Image();
        
        img.onload = function() {
            const ratio = Math.min(maxWidth / img.width, maxWidth / img.height);
            canvas.width = img.width * ratio;
            canvas.height = img.height * ratio;
            
            ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
            
            canvas.toBlob(resolve, 'image/jpeg', quality);
        };
        
        img.src = URL.createObjectURL(file);
    });
}

// Notification permission
function requestNotificationPermission() {
    if ('Notification' in window && Notification.permission === 'default') {
        Notification.requestPermission().then(permission => {
            console.log('Notification permission:', permission);
        });
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeVoiceRecognition();
    requestNotificationPermission();
    
    // Add smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
});

// Utility functions for Streamlit integration
function triggerStreamlitEvent(eventType, data) {
    // This would integrate with Streamlit's component system
    console.log('Streamlit event:', eventType, data);
}

// Export functions for Streamlit components
window.cookingAssistant = {
    startListening,
    stopListening,
    speakText,
    startTimer,
    stopTimer,
    scaleRecipe,
    compressImage
};