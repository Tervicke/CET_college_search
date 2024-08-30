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

document.getElementById('add-city').addEventListener('click', function() {
    const courseSelect = document.getElementById('city-select');
    const course = courseSelect.value.trim();
    if (course) {
        addTag('city-container', course);
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
			.map(tag => tag.textContent.trim().slice(0, -1).trim()); // Remove the "×" and trim

	const cities = Array.from(document.getElementById('city-container').children)
			.map(tag => tag.textContent.trim().slice(0, -1).trim()); // Remove the "×" and trim

	let has_error = false;

	clearErrors();	

	if(courses.length == 0){
		displayGlobalError("Please add atleast 1 course")
		has_error = true;
	}

	if(!minPercentile || !maxPercentile)	{
		displayGlobalError("Please fill the percentile fields")
		has_error = true;
	}
	if (minPercentile && maxPercentile && parseFloat(maxPercentile) < parseFloat(minPercentile)) {
		has_error = true;
		displayGlobalError("Make sure that min percentile < max percentile")
  }
	const jsonData = {
			mn: minPercentile,
			mx: maxPercentile,
			seattype: seatTypes,
			courses: courses,
			cities: cities
	};

  const jsonString = JSON.stringify(jsonData, null, 2);

    console.log(jsonString);
	if(!has_error){
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
}
function displayGlobalError(message) {
    const globalErrorElement = document.getElementById('global-error');
    globalErrorElement.textContent = message;
    globalErrorElement.style.display = 'block';
}

function clearErrors() {
    const globalErrorElement = document.getElementById('global-error');
    globalErrorElement.style.display = 'none';
    globalErrorElement.textContent = '';
}
