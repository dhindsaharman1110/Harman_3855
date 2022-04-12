import React, { useEffect, useState } from 'react'
import '../App.css';

export default function AppStats() {
    const [isLoaded, setIsLoaded] = useState(false);
    const [stats, setStats] = useState({});
    const [error, setError] = useState(null)

	const getStats = () => {
	
        fetch(`http://mykafka.eastus.cloudapp.azure.com/processing/stats`)
            .then(res => res.json())
            .then((result)=>{
				console.log("Received Stats")
                setStats(result);
                setIsLoaded(true);
            },(error) =>{
                setError(error)
                setIsLoaded(true);
            })
    }
    useEffect(() => {
		const interval = setInterval(() => getStats(), 2000); // Update every 2 seconds
		return() => clearInterval(interval);
    }, [getStats]);

    if (error){
        return (<div className={"error"}>Error found when fetching from API</div>)
    } else if (isLoaded === false){
        return(<div>Loading...</div>)
    } else if (isLoaded === true){
        return(
            <div>
                <h1>Latest Stats</h1>
                <table className={"StatsTable"}>
					<tbody>
						<tr>
							<th>Age</th>
							<th>Weight</th>
						</tr>
						<tr>
							<td># Age: {stats['num_a_g_readings']}</td>
							<td># Weight: {stats['num_h_w_readings']}</td>
						</tr>
						<tr>
							<td colspan="2">Max Age Reading: {stats['max_a_readings']}</td>
						</tr>
						<tr>
							<td colspan="2">Max Height: {stats['max_h_readings']}</td>
						</tr>
						<tr>
							<td colspan="2">Max Weight: {stats['max_w_readings']}</td>
						</tr>
					</tbody>
                </table>
                <h3>Last Updated: {stats['last_updateds']}</h3>

            </div>
        )
    }
}
