/**
 * Global Teardown for Playwright Tests
 * This file runs once after all tests are completed
 */

async function globalTeardown(config) {
  console.log('');
  console.log('🧹 Starting global teardown...');
  
  const fs = require('fs');
  const path = require('path');
  
  // Generate test summary
  try {
    const resultsPath = 'manual-tests/playwright/reports/results.json';
    if (fs.existsSync(resultsPath)) {
      const results = JSON.parse(fs.readFileSync(resultsPath, 'utf8'));
      
      console.log('📊 Test Execution Summary:');
      console.log(`   - Total tests: ${results.stats?.expected || 'N/A'}`);
      console.log(`   - Passed: ${results.stats?.passed || 0}`);
      console.log(`   - Failed: ${results.stats?.failed || 0}`);
      console.log(`   - Skipped: ${results.stats?.skipped || 0}`);
      console.log(`   - Duration: ${results.stats?.duration ? Math.round(results.stats.duration / 1000) + 's' : 'N/A'}`);
      
      if (results.stats?.failed > 0) {
        console.log('❌ Some tests failed. Check the HTML report for details.');
      } else {
        console.log('✅ All tests passed successfully!');
      }
    }
  } catch (error) {
    console.log('   ⚠️ Could not read test results file');
  }
  
  // Clean up old screenshots (keep only last 50)
  try {
    const screenshotsDir = 'manual-tests/playwright/screenshots';
    if (fs.existsSync(screenshotsDir)) {
      const files = fs.readdirSync(screenshotsDir)
        .filter(file => file.endsWith('.png'))
        .map(file => ({
          name: file,
          path: path.join(screenshotsDir, file),
          time: fs.statSync(path.join(screenshotsDir, file)).mtime.getTime()
        }))
        .sort((a, b) => b.time - a.time);
      
      if (files.length > 50) {
        const filesToDelete = files.slice(50);
        filesToDelete.forEach(file => {
          fs.unlinkSync(file.path);
        });
        console.log(`   🗑️ Cleaned up ${filesToDelete.length} old screenshot(s)`);
      }
    }
  } catch (error) {
    console.log('   ⚠️ Screenshot cleanup failed:', error.message);
  }
  
  // Log report locations
  console.log('📁 Test artifacts saved to:');
  console.log('   - HTML Report: manual-tests/playwright/reports/html/index.html');
  console.log('   - JSON Results: manual-tests/playwright/reports/results.json');
  console.log('   - JUnit XML: manual-tests/playwright/reports/results.xml');
  console.log('   - Screenshots: manual-tests/playwright/screenshots/');
  console.log('   - Videos: manual-tests/playwright/test-results/');
  
  console.log('✅ Global teardown completed');
}

module.exports = globalTeardown;
