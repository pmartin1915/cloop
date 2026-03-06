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
exports.UltrathinkService = void 0;
const vscode = __importStar(require("vscode"));
const path = __importStar(require("path"));
const child_process_1 = require("child_process");
const util_1 = require("util");
const execAsync = (0, util_1.promisify)(child_process_1.exec);
class UltrathinkService {
    constructor(context) {
        this.findings = [];
        this.patterns = [];
        this.context = context;
    }
    getUltrathinkCommand() {
        const config = vscode.workspace.getConfiguration('ultrathink');
        const ultrathinkPath = config.get('ultrathinkPath');
        if (ultrathinkPath) {
            return `cd "${ultrathinkPath}" && poetry run ultrathink`;
        }
        return 'poetry run ultrathink';
    }
    async runCommand(args) {
        const command = `${this.getUltrathinkCommand()} ${args}`;
        try {
            const { stdout, stderr } = await execAsync(command, {
                cwd: this.getWorkspacePath()
            });
            if (stderr && !stderr.includes('WARNING')) {
                console.error('Ultrathink stderr:', stderr);
            }
            return stdout;
        }
        catch (error) {
            throw new Error(`Command failed: ${error.message}`);
        }
    }
    getWorkspacePath() {
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders) {
            throw new Error('No workspace folder open');
        }
        return workspaceFolders[0].uri.fsPath;
    }
    async analyzeFile(filePath) {
        const output = await this.runCommand(`analyze --path "${filePath}" --save-findings`);
        await this.parseAnalysisOutput(output, filePath);
    }
    async analyzeWorkspace(workspacePath) {
        const output = await this.runCommand(`analyze --path "${workspacePath}" --save-findings`);
        await this.parseAnalysisOutput(output, workspacePath);
    }
    async learnPatterns(threshold) {
        const output = await this.runCommand(`learn --threshold ${threshold}`);
        // Parse output for pattern count
        const patternsMatch = output.match(/Patterns Identified:\s+(\d+)/);
        const patchesMatch = output.match(/Patches Generated:\s+(\d+)/);
        const patternsFound = patternsMatch ? parseInt(patternsMatch[1]) : 0;
        const patchesGenerated = patchesMatch ? parseInt(patchesMatch[1]) : 0;
        await this.loadPatterns();
        return { patternsFound, patchesGenerated };
    }
    async scaffoldProject(name, author, description) {
        const workspacePath = this.getWorkspacePath();
        const projectPath = path.join(workspacePath, name);
        await this.runCommand(`scaffold --name "${name}" --author "${author}" --description "${description}"`);
        return projectPath;
    }
    async getStats() {
        try {
            const output = await this.runCommand('stats');
            // Parse stats from output
            const findingsMatch = output.match(/Total findings:\s+(\d+)/);
            const patternsMatch = output.match(/Total patterns:\s+(\d+)/);
            const improvementsMatch = output.match(/Total improvements:\s+(\d+)/);
            const learningRateMatch = output.match(/Learning rate:\s+([\d.]+)%/);
            return {
                totalFindings: findingsMatch ? parseInt(findingsMatch[1]) : this.findings.length,
                totalPatterns: patternsMatch ? parseInt(patternsMatch[1]) : this.patterns.length,
                totalImprovements: improvementsMatch ? parseInt(improvementsMatch[1]) : 0,
                learningRate: learningRateMatch ? parseFloat(learningRateMatch[1]) : 0
            };
        }
        catch (error) {
            // Fallback to cached data
            return {
                totalFindings: this.findings.length,
                totalPatterns: this.patterns.length,
                totalImprovements: 0,
                learningRate: 0
            };
        }
    }
    async generateHandoff(filePath) {
        const config = vscode.workspace.getConfiguration('ultrathink');
        const profile = config.get('projectProfile') || 'auto';
        let cmd = `handoff --path "${filePath}"`;
        if (profile !== 'auto') {
            cmd += ` --profile ${profile}`;
        }
        const output = await this.runCommand(cmd);
        return output.trim();
    }
    getFindings() {
        return this.findings;
    }
    getPatterns() {
        return this.patterns;
    }
    async parseAnalysisOutput(output, basePath) {
        // Store findings from analysis
        // This is a simplified parser - in production, Ultrathink should output JSON
        this.findings = [];
        const lines = output.split('\n');
        for (const line of lines) {
            // Look for finding patterns in output
            if (line.includes('severity:') || line.includes('issue:')) {
                // Parse finding (simplified)
                this.findings.push({
                    file: basePath,
                    line: 0,
                    severity: 'medium',
                    category: 'quality',
                    description: line.trim(),
                    suggestion: 'See Ultrathink output for details'
                });
            }
        }
    }
    async loadPatterns() {
        // Load patterns from knowledge base
        // This would query the SQLite database in production
        this.patterns = [];
    }
}
exports.UltrathinkService = UltrathinkService;
//# sourceMappingURL=ultrathinkService.js.map