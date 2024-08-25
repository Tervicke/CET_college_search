document.getElementById('add-seat-type').addEventListener('click', function() {
    const seatTypeInput = document.getElementById('seat-type-input');
    const seatType = seatTypeInput.value.trim();
    if (seatType) {
        addTag('seat-types-container', seatType);
        seatTypeInput.value = '';
    }
});

document.getElementById('add-course').addEventListener('click', function() {
    const courseSelect = document.getElementById('course-select');
    const course = courseSelect.value.trim();
    if (course) {
        addTag('courses-container', course);
    }
});

function addTag(containerId, value) {
    const container = document.getElementById(containerId);
    const tag = document.createElement('div');
    tag.className = 'tag';
    tag.innerHTML = `
        ${value}
        <button type="button" class="remove-btn">&times;</button>
    `;
    container.appendChild(tag);
    attachRemoveHandler(tag);
}

function attachRemoveHandler(tagElement) {
    tagElement.querySelector('.remove-btn').addEventListener('click', function() {
        this.parentElement.remove();
    });
}

async function getSubmittedData() {
    const minPercentile = document.getElementById('min-percentile').value.trim();
    const maxPercentile = document.getElementById('max-percentile').value.trim();
    
    var seatTypes = Array.from(document.getElementById('seat-types-container').children)
        .map(tag => tag.textContent.trim().slice(0, -1).trim()); 

    seatTypes.push('GOPENH');
    seatTypes.push('GOPENS');

    const courses = Array.from(document.getElementById('courses-container').children)
        .map(tag => tag.textContent.trim().slice(0, -1).trim().toLowerCase()); // Remove the "×" and trim

    const jsonData = {
        mn: minPercentile,
        mx: maxPercentile,
        seattype: seatTypes,
        courses: courses
    };

    const jsonString = JSON.stringify(jsonData, null, 2);

    console.log(jsonString);

    try {
        const response = await fetch('/process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(jsonData)
        });
        console.log(response);
        if (response.ok) {
            window.location.href = '/result';
        } else {
            alert("ERROR");
        }
    } catch (error) {
        console.error('Fetch error:', error);
    }
}
