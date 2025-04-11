let previousData = "";
let expandedTranscripts = {};
let expandedSummaries = {};

function toggleTranscript(id) {
    let row = document.getElementById(id);
    row.style.display = row.style.display === "none" ? "table-row" : "none";
    expandedTranscripts[id] = row.style.display === "table-row";
}

function toggleSummary(id) {
    let row = document.getElementById(id);
    row.style.display = row.style.display === "none" ? "table-row" : "none";
    expandedSummaries[id] = row.style.display === "table-row";
}

function fetchData() {
    fetch("/api/conversations")
        .then(response => response.json())
        .then(data => {
            let newData = JSON.stringify(data.conversations);
            if (newData !== previousData) {
                previousData = newData;
                let tableBody = document.getElementById("table-body");
                tableBody.innerHTML = "";

                data.conversations.forEach((conv, index) => {
                    let rowIdTranscript = `transcript-${index}`;
                    let rowIdSummary = `summary-${index}`;
                    let statusClass = conv.appointment_status === "Booked" ? "status-booked" : "status-pending";

                    let row = `<tr>
                        <td>${conv.name}</td>
                        <td>${conv.phone}</td>
                        <td>${conv.email}</td>
                        <td>${conv.reason}</td>
                        <td>${conv.gender}</td>
                        <td>${conv.age}</td>
                        <td>${conv.city}</td>
                        <td>${conv.zip}</td>
                        <td>${conv.history}</td>
                        <td>${conv.date}</td>
                        <td>${conv.time}</td>
                        <td>${conv.referral}</td>
                        <td><span class="${statusClass}">${conv.appointment_status}</span></td>
                        <td><button class="expand-btn" onclick="toggleTranscript('${rowIdTranscript}')">View</button></td>
                        <td><button class="expand-btn" onclick="toggleSummary('${rowIdSummary}')">View</button></td>
                        <td>${conv.audio_file ? `<audio controls><source src="/api/audio/${conv.conversation_id}" type="audio/mpeg"></audio>` : "N/A"}</td>
                    </tr>
                    <tr id="${rowIdTranscript}" class="hidden-row" style="display: ${expandedTranscripts[rowIdTranscript] ? "table-row" : "none"};">
                        <td colspan="16">
                            <div class="transcript-container"><strong>Transcript:</strong><br>${conv.transcript}</div>
                        </td>
                    </tr>
                    <tr id="${rowIdSummary}" class="hidden-row" style="display: ${expandedSummaries[rowIdSummary] ? "table-row" : "none"};">
                        <td colspan="16">
                            <div class="summary-container"><strong>Summary:</strong><br>${conv.summary || "N/A"}</div>
                        </td>
                    </tr>`;
                    tableBody.innerHTML += row;
                });
            }
        })
        .catch(error => console.error("Error fetching data:", error));
}

fetchData();
setInterval(fetchData, 5000);
