"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.activate = activate;
exports.deactivate = deactivate;
const vscode = __importStar(require("vscode"));
const ultrathinkService_1 = require("./ultrathinkService");
const findingsProvider_1 = require("./views/findingsProvider");
const patternsProvider_1 = require("./views/patternsProvider");
const statsProvider_1 = require("./views/statsProvider");
let ultrathinkService;
let statusBarItem;
function activate(context) {
    console.log('Ultrathink extension activated');
    // Initialize service
    ultrathinkService = new ultrathinkService_1.UltrathinkService(context);
    // Create status bar item
    statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
    statusBarItem.command = 'ultrathink.showStats';
    statusBarItem.text = '$(lightbulb) Ultrathink';
    statusBarItem.tooltip = 'Click to view Ultrathink statistics';
    statusBarItem.show();
    context.subscriptions.push(statusBarItem);
    // Register tree data providers
    const findingsProvider = new findingsProvider_1.FindingsProvider(ultrathinkService);
    const patternsProvider = new patternsProvider_1.PatternsProvider(ultrathinkService);
    const statsProvider = new statsProvider_1.StatsProvider(ultrathinkService);
    vscode.window.registerTreeDataProvider('ultrathink.findingsView', findingsProvider);
    vscode.window.registerTreeDataProvider('ultrathink.patternsView', patternsProvider);
    vscode.window.registerTreeDataProvider('ultrathink.statsView', statsProvider);
    // Register commands
    context.subscriptions.push(vscode.commands.registerCommand('ultrathink.analyzeFile', async () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showWarningMessage('No active file to analyze');
            return;
        }
        const filePath = editor.document.uri.fsPath;
        await vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: 'Analyzing file with Ultrathink...',
            cancellable: false
        }, async () => {
            try {
                await ultrathinkService.analyzeFile(filePath);
                findingsProvider.refresh();
                updateStatusBar();
                vscode.window.showInformationMessage('Analysis complete! Check Ultrathink sidebar for findings.');
            }
            catch (error) {
                vscode.window.showErrorMessage(`Analysis failed: ${error}`);
            }
        });
    }));
    context.subscriptions.push(vscode.commands.registerCommand('ultrathink.analyzeWorkspace', async () => {
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders) {
            vscode.window.showWarningMessage('No workspace folder open');
            return;
        }
        const workspacePath = workspaceFolders[0].uri.fsPath;
        await vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: 'Analyzing workspace with Ultrathink...',
            cancellable: false
        }, async () => {
            try {
                await ultrathinkService.analyzeWorkspace(workspacePath);
                findingsProvider.refresh();
                updateStatusBar();
                vscode.window.showInformationMessage('Workspace analysis complete!');
            }
            catch (error) {
                vscode.window.showErrorMessage(`Analysis failed: ${error}`);
            }
        });
    }));
    context.subscriptions.push(vscode.commands.registerCommand('ultrathink.learnPatterns', async () => {
        const threshold = await vscode.window.showInputBox({
            prompt: 'Minimum pattern frequency (default: 2)',
            value: '2',
            validateInput: (value) => {
                const num = parseInt(value);
                return isNaN(num) || num < 1 ? 'Please enter a valid number >= 1' : null;
            }
        });
        if (!threshold) {
            return;
        }
        await vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: 'Learning patterns...',
            cancellable: false
        }, async () => {
            try {
                const result = await ultrathinkService.learnPatterns(parseInt(threshold));
                patternsProvider.refresh();
                updateStatusBar();
                vscode.window.showInformationMessage(`Learned ${result.patternsFound} patterns, generated ${result.patchesGenerated} patches`);
            }
            catch (error) {
                vscode.window.showErrorMessage(`Learning failed: ${error}`);
            }
        });
    }));
    context.subscriptions.push(vscode.commands.registerCommand('ultrathink.scaffoldProject', async () => {
        const projectName = await vscode.window.showInputBox({
            prompt: 'Project name',
            placeHolder: 'my-api'
        });
        if (!projectName) {
            return;
        }
        const author = await vscode.window.showInputBox({
            prompt: 'Author name',
            placeHolder: 'Your Name'
        });
        const description = await vscode.window.showInputBox({
            prompt: 'Project description',
            placeHolder: 'A FastAPI microservice'
        });
        await vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: 'Scaffolding project...',
            cancellable: false
        }, async () => {
            try {
                const projectPath = await ultrathinkService.scaffoldProject(projectName, author || 'Developer', description || 'A new project');
                const openFolder = await vscode.window.showInformationMessage(`Project created at ${projectPath}`, 'Open Folder');
                if (openFolder === 'Open Folder') {
                    vscode.commands.executeCommand('vscode.openFolder', vscode.Uri.file(projectPath));
                }
            }
            catch (error) {
                vscode.window.showErrorMessage(`Scaffolding failed: ${error}`);
            }
        });
    }));
    context.subscriptions.push(vscode.commands.registerCommand('ultrathink.showStats', async () => {
        const stats = await ultrathinkService.getStats();
        const message = `
Ultrathink Statistics:
• Findings: ${stats.totalFindings}
• Patterns: ${stats.totalPatterns}
• Improvements: ${stats.totalImprovements}
• Learning Rate: ${stats.learningRate}%
            `.trim();
        vscode.window.showInformationMessage(message, { modal: true });
    }));
    context.subscriptions.push(vscode.commands.registerCommand('ultrathink.refreshFindings', () => {
        findingsProvider.refresh();
        patternsProvider.refresh();
        statsProvider.refresh();
    }));
    context.subscriptions.push(vscode.commands.registerCommand('ultrathink.generateHandoff', async () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showWarningMessage('No active file');
            return;
        }
        await vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: 'Generating Amazon Q handoff...',
            cancellable: false
        }, async () => {
            try {
                const handoff = await ultrathinkService.generateHandoff(editor.document.uri.fsPath);
                await vscode.env.clipboard.writeText(handoff);
                const action = await vscode.window.showInformationMessage('✓ Handoff copied! Paste into Amazon Q.', 'Open Q', 'View');
                if (action === 'Open Q') {
                    vscode.commands.executeCommand('aws.amazonq.focusChat');
                }
                else if (action === 'View') {
                    const doc = await vscode.workspace.openTextDocument({
                        content: handoff,
                        language: 'markdown'
                    });
                    await vscode.window.showTextDocument(doc);
                }
            }
            catch (error) {
                vscode.window.showErrorMessage(`Failed: ${error}`);
            }
        });
    }));
    // Auto-analyze on save if enabled
    context.subscriptions.push(vscode.workspace.onDidSaveTextDocument(async (document) => {
        const config = vscode.workspace.getConfiguration('ultrathink');
        if (config.get('autoAnalyze') && document.languageId === 'python') {
            await ultrathinkService.analyzeFile(document.uri.fsPath);
            findingsProvider.refresh();
            updateStatusBar();
        }
    }));
    // Initial status update
    updateStatusBar();
}
function updateStatusBar() {
    ultrathinkService.getStats().then(stats => {
        statusBarItem.text = `$(lightbulb) ${stats.totalPatterns} patterns`;
        statusBarItem.tooltip = `Ultrathink: ${stats.totalFindings} findings, ${stats.totalPatterns} patterns learned`;
    });
}
function deactivate() {
    if (statusBarItem) {
        statusBarItem.dispose();
    }
}
//# sourceMappingURL=extension.js.map