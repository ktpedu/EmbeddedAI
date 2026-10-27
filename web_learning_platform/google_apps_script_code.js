/**
 * Google Apps Script สำหรับระบบบันทึกการส่งงานและคะแนนประเมิน (EdgeAI Learning Platform)
 * แผ่นงานเป้าหมายแยกเป็น 2 ชีตอย่างชัดเจน:
 * 1. practical (สำหรับโจทย์ข้อสอบปฏิบัติ - พร้อมคะแนนประเมินรูบริกเต็ม 10 คะแนน)
 * 2. worksheet (สำหรับใบงานปฏิบัติการประจำบท)
 *
 * * มีระบบค้นหาและสร้างแท็บชีตให้อัตโนมัติ (รองรับทั้งชื่ออังกฤษ practical/worksheet และภาษาไทย โจทย์ปฏิบัติ/ใบงาน)
 * * หัวตารางมาตรฐาน 9 คอลัมน์ (A - I) ในแต่ละชีต
 */

function doPost(e) {
  var lock = LockService.getScriptLock();
  lock.tryLock(30000);

  try {
    var contents = e.postData ? e.postData.contents : "";
    var data = {};
    try {
      data = JSON.parse(contents);
    } catch (parseErr) {
      data = e.parameter || {};
    }

    var action = (data.action || "submission").toLowerCase();
    var taskType = (data.task_type || "practical").toLowerCase();
    var requestedSheetName = data.sheet_name || (taskType === "worksheet" ? "worksheet" : "practical");

    var ss = SpreadsheetApp.getActiveSpreadsheet();
    
    // ค้นหาชีตเป้าหมาย หรือสร้างแท็บชีตใหม่หากยังไม่มี
    function getTargetSheet(ss, reqName) {
      var isWs = (reqName.toLowerCase().indexOf("work") !== -1 || reqName.indexOf("ใบงาน") !== -1 || taskType === "worksheet");
      
      if (isWs) {
        var ws = ss.getSheetByName("worksheet") || ss.getSheetByName("ใบงาน") || ss.getSheetByName("lab_worksheet");
        if (ws) return { sheet: ws, isWorksheet: true };
        return { sheet: ss.insertSheet("worksheet"), isWorksheet: true };
      } else {
        var ps = ss.getSheetByName("practical") || ss.getSheetByName("โจทย์ปฏิบัติ") || ss.getSheetByName("practical_exam");
        if (ps) return { sheet: ps, isWorksheet: false };
        return { sheet: ss.insertSheet("practical"), isWorksheet: false };
      }
    }

    var targetInfo = getTargetSheet(ss, requestedSheetName);
    var sheet = targetInfo.sheet;
    var isWorksheet = targetInfo.isWorksheet;

    // หัวตารางมาตรฐาน 9 คอลัมน์ (A - I)
    var headers = [
      "วัน-เวลาที่ส่ง (Timestamp)",
      "รหัสนักเรียน (StudentID)",
      "ชื่อ-นามสกุล (Name)",
      "บทเรียน (Chapter)",
      isWorksheet ? "ลิงก์ส่งใบงานประจำบท (Worksheet URL)" : "ลิงก์ส่งโจทย์ปฏิบัติ (Practical URL)",
      "บันทึกสรุปผล (Notes)",
      "คะแนนที่ได้ (Score)",
      "ข้อเสนอแนะครูผู้ประเมิน (Teacher Feedback)",
      "เวลาที่ประเมินคะแนน (Graded At)"
    ];

    var lastRow = sheet.getLastRow();
    var lastCol = sheet.getLastColumn();

    if (lastRow === 0) {
      sheet.appendRow(headers);
      sheet.getRange(1, 1, 1, headers.length).setBackground("#1a73e8").setFontColor("#ffffff").setFontWeight("bold");
    } else {
      var currentHeaders = sheet.getRange(1, 1, 1, Math.max(lastCol, 10)).getValues()[0];
      // ตรวจสอบกรณีชีตเดิมมี 10 คอลัมน์จากการรวมก่อนหน้า
      if (isWorksheet && currentHeaders[4] && String(currentHeaders[4]).indexOf("โจทย์") !== -1 && currentHeaders[5] && String(currentHeaders[5]).indexOf("ใบงาน") !== -1) {
        sheet.deleteColumn(5); // ลบคอลัมน์โจทย์ปฏิบัติออกจากชีตใบงาน เพื่อให้คอลัมน์ใบงานอยู่ที่คอลัมน์ 5
      } else if (!isWorksheet && currentHeaders[4] && String(currentHeaders[4]).indexOf("โจทย์") !== -1 && currentHeaders[5] && String(currentHeaders[5]).indexOf("ใบงาน") !== -1) {
        sheet.deleteColumn(6); // ลบคอลัมน์ใบงานออกจากชีตโจทย์ปฏิบัติ
      }

      // บันทึกหัวคอลัมน์มาตรฐาน 9 คอลัมน์
      for (var c = 0; c < headers.length; c++) {
        sheet.getRange(1, c + 1).setValue(headers[c]);
      }
      sheet.getRange(1, 1, 1, headers.length).setBackground("#1a73e8").setFontColor("#ffffff").setFontWeight("bold");
    }

    // Dynamic column finding
    var activeHeaders = sheet.getRange(1, 1, 1, Math.max(sheet.getLastColumn(), 9)).getValues()[0];
    function findCol(keywords, fallback) {
      for (var i = 0; i < activeHeaders.length; i++) {
        var str = String(activeHeaders[i] || "").toLowerCase();
        for (var k = 0; k < keywords.length; k++) {
          if (str.indexOf(keywords[k].toLowerCase()) !== -1) return i + 1;
        }
      }
      return fallback;
    }

    var colTimestamp = findCol(["timestamp", "วัน-เวลา"], 1);
    var colStudentId = findCol(["studentid", "รหัสนักเรียน"], 2);
    var colStudentName = findCol(["name", "ชื่อ-นามสกุล"], 3);
    var colChapter = findCol(["chapter", "บทเรียน"], 4);
    var colUrl = findCol(["url", "ลิงก์", "รายงาน", "ใบงาน"], 5);
    var colNotes = findCol(["notes", "บันทึกสรุป"], 6);
    var colScore = findCol(["score", "คะแนน"], 7);
    var colFeedback = findCol(["feedback", "ข้อเสนอแนะ"], 8);
    var colGradedAt = findCol(["graded at", "เวลาที่ประเมิน"], 9);

    var studentId = String(data.student_id || "").trim();
    var studentName = String(data.student_name || "").trim();
    var chapter = String(data.chapter_id || "").trim();
    var chapterCode = String(data.chapter_code || "").trim();
    var unitNum = data.unit_number;
    var timestamp = data.timestamp || Utilities.formatDate(new Date(), "Asia/Bangkok", "dd/MM/yyyy HH:mm:ss");

    lastRow = sheet.getLastRow();
    var targetRowIndex = -1;

    // ค้นหาแถวของนักเรียนและบทเรียนนี้ในชีต (ตั้งแต่แถวที่ 2 เป็นต้นไป)
    if (lastRow > 1 && studentId) {
      var numColsToRead = Math.max(sheet.getLastColumn(), 9);
      var rangeValues = sheet.getRange(2, 1, lastRow - 1, numColsToRead).getValues();

      for (var i = 0; i < rangeValues.length; i++) {
        var rowStudentId = String(rangeValues[i][colStudentId - 1]).trim();
        var rowChapter = String(rangeValues[i][colChapter - 1]).trim();

        if (rowStudentId === studentId) {
          var matched = false;
          if (rowChapter === chapter) {
            matched = true;
          } else if (unitNum && (rowChapter.indexOf("บทที่ " + unitNum) !== -1 || rowChapter.indexOf("Unit " + unitNum) !== -1)) {
            matched = true;
          } else if (chapterCode && (rowChapter.indexOf(chapterCode) !== -1 || chapter.indexOf(chapterCode) !== -1)) {
            matched = true;
          } else if (chapter && rowChapter && (chapter.indexOf(rowChapter) !== -1 || rowChapter.indexOf(chapter) !== -1)) {
            matched = true;
          }

          if (matched) {
            targetRowIndex = i + 2;
            break;
          }
        }
      }
    }

    // กรณีครูบันทึกคะแนน (Action: 'grade')
    if (action === "grade") {
      var scoreVal = data.score_display || (data.score !== undefined ? data.score + " / " + (data.max_score || 10) : "");
      var teacherNotes = data.teacher_notes || "";
      var gradedAt = timestamp;

      if (targetRowIndex > 0) {
        sheet.getRange(targetRowIndex, colScore).setValue(scoreVal);
        sheet.getRange(targetRowIndex, colFeedback).setValue(teacherNotes);
        sheet.getRange(targetRowIndex, colGradedAt).setValue(gradedAt);
        sheet.getRange(targetRowIndex, colScore).setBackground("#e6f4ea");

        if (data.report_url || data.practical_url) {
          var currUrl = String(sheet.getRange(targetRowIndex, colUrl).getValue() || "").trim();
          if (!currUrl || currUrl === "-") sheet.getRange(targetRowIndex, colUrl).setValue(data.report_url || data.practical_url);
        }

        return ContentService.createTextOutput(JSON.stringify({
          status: "success",
          action: "grade_updated",
          sheet_name: sheet.getName(),
          row: targetRowIndex,
          score: scoreVal,
          message: "อัปเดตคะแนนของ " + studentName + " (" + scoreVal + ") ลงชีต " + sheet.getName() + " แถวที่ " + targetRowIndex + " สำเร็จ"
        })).setMimeType(ContentService.MimeType.JSON);
      } else {
        var newRow = [
          timestamp,
          studentId,
          studentName,
          chapter,
          data.report_url || data.practical_url || "-",
          "ประเมินจากระบบผู้สอน",
          scoreVal,
          teacherNotes,
          gradedAt
        ];
        sheet.appendRow(newRow);
        var addedRow = sheet.getLastRow();
        sheet.getRange(addedRow, colScore).setBackground("#e6f4ea");

        return ContentService.createTextOutput(JSON.stringify({
          status: "success",
          action: "grade_appended",
          sheet_name: sheet.getName(),
          row: addedRow,
          score: scoreVal,
          message: "บันทึกคะแนนของ " + studentName + " (" + scoreVal + ") ในชีต " + sheet.getName() + " แถวใหม่ที่ " + addedRow + " สำเร็จ"
        })).setMimeType(ContentService.MimeType.JSON);
      }
    } else {
      // กรณีนักเรียนส่งงาน (Action: 'submission')
      var reportUrl = String(data.report_url || (isWorksheet ? data.worksheet_url : data.practical_url) || "").trim();
      var notes = String(data.notes || "").trim();

      if (targetRowIndex > 0) {
        sheet.getRange(targetRowIndex, colTimestamp).setValue(timestamp);
        if (studentName) sheet.getRange(targetRowIndex, colStudentName).setValue(studentName);
        if (chapter) sheet.getRange(targetRowIndex, colChapter).setValue(chapter);
        if (reportUrl) sheet.getRange(targetRowIndex, colUrl).setValue(reportUrl);
        if (notes) sheet.getRange(targetRowIndex, colNotes).setValue(notes);

        return ContentService.createTextOutput(JSON.stringify({
          status: "success",
          action: "submission_updated",
          sheet_name: sheet.getName(),
          row: targetRowIndex,
          task_type: taskType,
          message: "อัปเดตการส่งงานลงชีต " + sheet.getName() + " ของ " + studentName + " ในแถวที่ " + targetRowIndex + " สำเร็จ"
        })).setMimeType(ContentService.MimeType.JSON);
      } else {
        // ส่งงานครั้งแรก เพิ่มแถวใหม่ 9 คอลัมน์
        var newSubRow = [
          timestamp,
          studentId,
          studentName,
          chapter,
          reportUrl || "-",
          notes || "-",
          "", // คะแนน (รอตรวจ)
          "", // ข้อเสนอแนะ
          ""  // เวลาที่ตรวจ
        ];

        sheet.appendRow(newSubRow);

        return ContentService.createTextOutput(JSON.stringify({
          status: "success",
          action: "submission_created",
          sheet_name: sheet.getName(),
          row: sheet.getLastRow(),
          task_type: taskType,
          message: "บันทึกการส่งงานใหม่ลงชีต " + sheet.getName() + " ของ " + studentName + " สำเร็จ"
        })).setMimeType(ContentService.MimeType.JSON);
      }
    }
  } catch (error) {
    return ContentService.createTextOutput(JSON.stringify({
      status: "error",
      message: error.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  } finally {
    lock.releaseLock();
  }
}

function doGet(e) {
  return ContentService.createTextOutput(JSON.stringify({
    status: "online",
    service: "EdgeAI Learning Platform - Multi-Sheet Sync Webhook",
    sheets_supported: [
      { name: "practical", description: "โจทย์ข้อสอบปฏิบัติ (พร้อมคะแนนประเมิน 10 คะแนน)" },
      { name: "worksheet", description: "ใบงานปฏิบัติการประจำบท" }
    ],
    timestamp: new Date().toISOString()
  })).setMimeType(ContentService.MimeType.JSON);
}
