function sendExtractedData() {
  const data = extractExistingData();
  const sheetName = 'BRED';  // Replace with your actual sheet name or logic to get sheet name
  const url = 'https://coral-app-kajof.ondigitalocean.app/google-sheet-webhook/';
  const headers = {
    "Api-Key": "1x#oa#itygde9_y(t3w=ju@-axdhq=@dyk1=wyp89nubgmh^dh"
  };
  const payload = {
    data: data,
    sheet_name: sheetName
  };
  const options = {
    'method': 'post',
    'contentType': 'application/json',
    'headers': headers,
    'payload': JSON.stringify(payload),
    'muteHttpExceptions': true
  };

  try {
    const response = UrlFetchApp.fetch(url, options);
    Logger.log(response.getContentText());
  } catch (error) {
    Logger.log(`Error: ${error.toString()}`);
  }
}

function extractExistingData() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  const numRows = sheet.getLastRow();
  const numColumns = sheet.getLastColumn();
  const headers = sheet.getSheetValues(1, 1, 1, numColumns)[0];
  const data = sheet.getSheetValues(2, 1, numRows - 1, numColumns);
  const dataList = data.map(row => {
    let rowObject = {};
    row.forEach((value, index) => {
      rowObject[headers[index]] = value.toString().replace(/\t/g, '').trim();
    });
    return rowObject;
  });

  Logger.log(`Extracted Data: ${JSON.stringify(dataList)}`);
  return dataList;
}


function runOnEdit(e) {
  const range = e.range;
  const sheet = range.getSheet();
  const sheetName = sheet.getName();
  const rowIndex = range.getRow();
  const numColumns = sheet.getLastColumn();
  const values = sheet.getSheetValues(rowIndex, 1, 1, numColumns)[0];
  const headersData = sheet.getSheetValues(1, 1, 1, numColumns)[0];

  Logger.log(`Values: ${values}`);
  Logger.log(`Headers: ${headersData}`);
  Logger.log(`Sheet Name: ${sheetName}`);

  if (values.filter(a => a).length < numColumns) {
    Logger.log("Incomplete row");
    return;
  }

  const dataList = [];
  const dataObject = {};
  headersData.forEach((header, index) => {
    dataObject[header] = values[index].toString().replace(/\t/g, '').trim();
  });
  dataList.push(dataObject);

  const data = {
    data: dataList,  // Wrap dataList in a 'data' key
    sheet_name: sheetName
  };

  Logger.log("Sending request");
  const url = 'https://coral-app-kajof.ondigitalocean.app/google-sheet-webhook/';
  const headers = {
    "Api-Key": "1x#oa#itygde9_y(t3w=ju@-axdhq=@dyk1=wyp89nubgmh^dh"
  };

  const options = {
    'method': 'post',
    'contentType': 'application/json',
    'headers': headers,
    'payload': JSON.stringify(data),
    'muteHttpExceptions': true
  };

  try {
    const response = UrlFetchApp.fetch(url, options);
    Logger.log(response.getContentText());
  } catch (error) {
    Logger.log(`Error: ${error.toString()}`);
  }
}
