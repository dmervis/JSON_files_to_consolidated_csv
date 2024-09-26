# Function to display progress
function Show-Progress {
    param (
        [int]$Current,
        [int]$Total
    )
    $percent = [math]::Round(($Current / $Total) * 100)
    $statusBar = "=" * ($percent / 5)  # Each "=" represents 5%
    $statusBar += " " * (20 - ($percent / 5))  # Fill to 20 characters
    Write-Progress -Activity "Processing files" -Status "$Current of $Total files processed" -PercentComplete $percent
}

# Prompt for folder path and output CSV path
$folderPath = Read-Host "Enter the folder path containing JSON files"
$outputCsvPath = Read-Host "Enter the output CSV file path (including filename.csv)"

# Initialize an empty array to hold all the data
$allData = @()

# Get all JSON files in the specified folder
$jsonFiles = Get-ChildItem -Path $folderPath -Filter *.json

# Check if any JSON files are found
if ($jsonFiles.Count -eq 0) {
    Write-Host "No JSON files found in the specified folder."
    exit
}

# Loop through each JSON file and process
$totalFiles = $jsonFiles.Count
for ($i = 0; $i -lt $totalFiles; $i++) {
    $jsonFile = $jsonFiles[$i]
    
    # Read the JSON content
    $jsonContent = Get-Content -Path $jsonFile.FullName -Raw | ConvertFrom-Json
    
    # Add the data to the allData array
    $allData += $jsonContent
    
    # Update progress
    Show-Progress -Current ($i + 1) -Total $totalFiles
}

# Convert the combined data to CSV and export it
$allData | Export-Csv -Path $outputCsvPath -NoTypeInformation -Encoding UTF8

Write-Host "Consolidation complete! CSV file created at: $outputCsvPath"
