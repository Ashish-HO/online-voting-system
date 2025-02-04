document.addEventListener('DOMContentLoaded', function() {
  console.log(djangoData);  // This should now work and log: 'This is some data from Django'
  // Use the data as needed
  document.getElementById("someElement").innerText = djangoData;
});
const sidebar = document.getElementById("sidebar");
const content = document.getElementById("content");
const toggleBtn = document.getElementById("toggleBtn");

toggleBtn.addEventListener("click", () => {
  sidebar.classList.toggle("collapsed");
  content.classList.toggle("collapsed");
});

const positions = [
  {
    title: "President",
    candidates: [
      {
        name: "Alice",
        photo:
          "https://media.gettyimages.com/id/1233975757/photo/former-prime-minister-k-p-sharma-oli-waves-as-he-arrives-at-his-private-residence-after-being.jpg?s=612x612&w=0&k=20&c=HaayXHs4XSIdGB1zy9FCb-U8Yynv-XepaoF630N5BVM=",
      },
      { name: "Bob", photo: "bob.jpg" },
      { name: "Charlie", photo: "charlie.jpg" },
      { name: "Diana", photo: "diana.jpg" },

      {
        name: "Charlie",
        photo:
          "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSSkNxfcYoNC4mSd983lj8xXHAC-8ee2mGLbQSnqAv9hDR8yQGiVDrM2e6byF1yw5KBiO_CItBMCG0dBrK-sUazQQ",
      },
    ],
  },
  {
    title: "Vice-President",
    candidates: [
      { name: "Eve", photo: "eve.jpg" },
      { name: "Frank", photo: "frank.jpg" },
      { name: "Grace", photo: "grace.jpg" },
      { name: "Hank", photo: "hank.jpg" },
    ],
  },
  {
    title: "Secretary",
    candidates: [
      { name: "Eve", photo: "eve.jpg" },
      { name: "Frank", photo: "frank.jpg" },
      { name: "Grace", photo: "grace.jpg" },
      { name: "Hank", photo: "hank.jpg" },
    ],
  },
  {
    title: "Member",
    candidates: [
      { name: "Eve", photo: "eve.jpg" },
      { name: "Frank", photo: "frank.jpg" },
      { name: "Grace", photo: "grace.jpg" },
      { name: "Hank", photo: "hank.jpg" },
    ],
  },
];

const positionsContainer = document.getElementById("positions");

positions.forEach((position) => {
  const positionDiv = document.createElement("div");
  positionDiv.classList.add("position");
  const positionTitle = document.createElement("h2");
  positionTitle.textContent = position.title;
  positionDiv.appendChild(positionTitle);

  const candidatesDiv = document.createElement("div");
  candidatesDiv.classList.add("candidates");

  position.candidates.forEach((candidate) => {
    const candidateDiv = document.createElement("div");
    candidateDiv.classList.add("candidate");
    candidateDiv.innerHTML = `
      <img src="${candidate.photo}" alt="${candidate.name}" style="width:80px; height:80px; border-radius:50%;">
      <h3>${candidate.name}</h3>`;

    candidateDiv.addEventListener("click", () => {
      // Toggle the "active" class for individual candidates
      candidateDiv.classList.toggle("active");

      // Ensure only one candidate per position has the "active" class
      Array.from(candidatesDiv.children).forEach((child) => {
        if (child !== candidateDiv) {
          child.classList.remove("active");
        }
      });
    });
    candidatesDiv.appendChild(candidateDiv);
  });

  positionDiv.appendChild(candidatesDiv);
  positionsContainer.appendChild(positionDiv);
});

// Process votes on Submit button click
const submitBtn = document.getElementById("submitVotes");
const resultsContainer = document.getElementById("results");

submitBtn.addEventListener("click", () => {
  const votes = {};

  thankYouPopup.classList.add("show");
  seeMyVotesBtn.addEventListener("click", () => {
    window.location.href = 'result/';  //add url here
  });
  // Loop through positions and extract active candidates
  document.querySelectorAll(".position").forEach((positionDiv) => {
    const positionTitle = positionDiv.querySelector("h2").textContent;
    const activeCandidate = positionDiv.querySelector(".candidate.active");

    if (activeCandidate) {
      const candidateName = activeCandidate.querySelector("h3").textContent;
      const candidatePhoto = activeCandidate.querySelector("img").src;
      votes[positionTitle] = { name: candidateName, photo: candidatePhoto };
    } else {
      votes[positionTitle] = { name: "No vote cast", photo: "" };
    }
  });
  console.log("Votes:", votes);
  localStorage.setItem("votes", JSON.stringify(votes));
  // Clear and display results dynamically in the results container
  resultsContainer.innerHTML = "<h3>Results</h3>";
  for (const [position, { name, photo }] of Object.entries(votes)) {
    resultsContainer.innerHTML += `
      <div class="result">
        <h4>${position}:</h4>
        ${
          photo
            ? `<img src="${photo}" alt="${name}" style="width:50px; height:50px; border-radius:50%;">`
            : ""
        }
        <p>${name}</p>
        
      </div>`;
  }
});

document.addEventListener("DOMContentLoaded", () => {
  const userIdElement = document.getElementById("userId");
  const userId = "Sarad2025";
  if (userIdElement) userIdElement.textContent = userId;
});

const thankYouPopup = document.getElementById("thankYouPopup");
const seeMyVotesBtn = document.getElementById("seeMyVotesBtn");

// Redirect to results page when "See My Votes" is clicked
