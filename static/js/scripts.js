// Script for Client-Side Interactivity

document.addEventListener("DOMContentLoaded", () => {
     const uploadForm = document.querySelector("form");
     const fileInput = document.getElementById("file");
     const allowedExtensions = ["pdf", "docx"];
     
     // Event listener for form submission
     uploadForm.addEventListener("submit", (event) => {
       const file = fileInput.files[0];
       
       // Check if a file is selected
       if (!file) {
         alert("Please select a file before submitting.");
         event.preventDefault();
         return;
       }
   
       // Validate file extension
       const fileExtension = file.name.split(".").pop().toLowerCase();
       if (!allowedExtensions.includes(fileExtension)) {
         alert(`Invalid file type. Please upload a file with one of the following extensions: ${allowedExtensions.join(", ")}`);
         event.preventDefault();
       }
     });
   });
   