// Example of a React function component using hooks
/*import React, { useState, useEffect } from 'react';

function DataViewer() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch('http://localhost:8000/scan', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        include_schema_regex: ["^crm$"],
        exclude_schema_regex: ["^sakila$", "^world$"]
      })
    })
      .then(response => response.json())
      .then(setData)
      .catch(console.error);
  }, []);

  
  return (
    <div>
        <h1 style={{ textAlign: 'center' }}>PII Database Scan Results</h1>
        <table>
            <thead>
                <tr>
                    <th>Database</th>
                    <th>Table</th>
                    <th>Column</th>
                    <th>Type</th>
                    <th>Detector</th>
                </tr>
            </thead>
            <tbody>
                {data.map((item, index) => (
                    <tr key={index}>
                        <td>{item[0]}</td>
                        <td>{item[1]}</td>
                        <td>{item[2]}</td>
                        <td>{item[3]}</td>
                        <td>{item[4]}</td>
                    </tr>
                ))}
            </tbody>
        </table>
    </div>
);
}

export default DataViewer; */
//End of Ruhuma's file

import React, { useState, useEffect } from 'react';
import './components/Data.css';
//import axios from 'axios';

function DataViewer() {
  const [data, setData] = useState([]);
  const [databases, setDatabases] = useState([]);
  const [selectedDatabase, setSelectedDatabase] = useState('');
  const [tables, setTables] = useState([]);
  const [selectedTable, setSelectedTable] = useState('');
  
  useEffect(() => {
    // Fetch list of databases
    fetch('http://127.0.0.1:8000/databases')
      .then(response => response.json())
      .then(data => {
        // Extract the databases array from the response data and set it in state
        setDatabases(data.databases);
      })
      .catch(error => {
        console.error('Error fetching databases:', error);
      });
  }, []);

// Fetch tables for the selected database
useEffect(() => {
  if (selectedDatabase) {
    fetch(`http://localhost:8000/tables/${selectedDatabase}`)
      .then(response => response.json())
      .then(data => {
        setTables(data.tables);
      })
      .catch(error => {
        console.error(`Error fetching tables for database ${selectedDatabase}:`, error);
      });
  }
}, [selectedDatabase]);

// Handle database selection change
const handleDatabaseChange = (event) => {
  setSelectedDatabase(event.target.value);
};

// Handle table selection change
const handleTableChange = (event) => {
  setSelectedTable(event.target.value);
};


 
  useEffect(() => {
    // Check if both selectedDatabase and selectedTable have values
  if (selectedDatabase && selectedTable) {
    fetch('http://localhost:8000/scan', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        include_schema_regex: selectedDatabase,
        include_table_regex: selectedTable
      })
    })
      .then(response => response.json())
      .then(setData)
      .catch(console.error);
  }
  }, [selectedDatabase, selectedTable]);

  
  return (
    
    <div className="user-data-container">
        <h1 >PII Catcher UI</h1>
       
      <div>
  <table style={{ marginLeft: '150px',marginBottom: '15px'}}>
    <tbody>
      <tr>
        <td style={{ verticalAlign: 'top' }}>
          <h4>Databases</h4>
          <select value={selectedDatabase} onChange={handleDatabaseChange}>
            <option value="">Select a database...</option>
            {databases.map((database, index) => (
              <option key={index} value={database}>{database}</option>
            ))}
          </select>
        </td>
        <td style={{ verticalAlign: 'top' }}>
          {selectedDatabase && (
            <div>
              <h4>Tables in {selectedDatabase}</h4>
              <select value={selectedTable} onChange={handleTableChange}>
                <option value="">Select a table</option>
                {tables.map((table, index) => (
                  <option key={index} value={table}>
                    {table}
                  </option>
                ))}
              </select>
            </div>
          )}
        </td>
      </tr>
    </tbody>
  </table>
</div>
        <table  className="user-table" >
            <thead>
                <tr>
                    <th>Database</th>
                    <th>Table</th>
                    <th>Field</th>
                    <th>PIILevel</th>
                    <th>Class</th>
                </tr>
            </thead>
            <tbody>
                {data.map((item, index) => (
                    <tr key={index}>
                        <td>{item.database}</td>
                        <td>{item.table}</td>
                        <td>{item.field}</td>
                        <td>{item.PIILevel}</td>
                        <td>{item.Class}</td>
                    </tr>
                ))}
            </tbody>
        </table>
    </div>
);
}
export default DataViewer; 