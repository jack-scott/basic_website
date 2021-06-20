

export function getSolutions() {
    // const result = .then((result)=>{console.log(result)})
    // fetch('http://example.com/movies.json%27)
  
    return fetch("http://localhost:5000/solutions?q=hello", {
    headers: {
        "Accept": 'application/json',
    }}).then(response => {
        return response.clone().json()
    })
    .catch(console.log)
}