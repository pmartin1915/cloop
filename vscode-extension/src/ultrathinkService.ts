import * as vscode from 'vscode';
import * as path from 'path';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

export interface Finding {
    file: string;
    line: number;
    severity: string;
    category: string;
    description: string;
    suggestion: string;
}

export interface Pattern {
    id: number;
    category: string;
    description: string;
    frequency: number;
}

export interface Stats {
    totalFindings: number;
    totalPatterns: number;
    totalImprovements: number;
    learningRate: number;
}

export class UltrathinkService {
    private context: vscode.ExtensionContext;
    private findings: Finding[] = [];
    private patterns: Pattern[] = [];

    constructor(context: vscode.ExtensionContext) {
        this.context = context;
    }

    private getUltrathinkCommand(): string {
        const config = vscode.workspace.getConfiguration('ultrathink');
        const ultrathinkPath = config.get<string>('ultrathinkPath');
        
        if (ultrathinkPath) {
            return `cd "${ultrathinkPath}" && poetry run ultrathink`;
        }
        
        return 'poetry run ultrathink';
    }

    private async runCommand(args: string): Promise<string> {
        const command = `${this.getUltrathinkCommand()} ${args}`;
        
        try {
            const { stdout, stderr } = await execAsync(command, {
                cwd: this.getWorkspacePath()
            });
            
            if (stderr && !stderr.includes('WARNING')) {
                console.error('Ultrathink stderr:', stderr);
            }
            
            return stdout;
        } catch (error: any) {
            throw new Error(`Command failed: ${error.message}`);
        }
    }

    private getWorkspacePath(): string {
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders) {
            throw new Error('No workspace folder open');
        }
        return workspaceFolders[0].uri.fsPath;
    }

    async analyzeFile(filePath: string): Promise<void> {
        const output = await this.runCommand(`analyze --path "${filePath}" --save-findings`);
        await this.parseAnalysisOutput(output, filePath);
    }

    async analyzeWorkspace(workspacePath: string): Promise<void> {
        const output = await this.runCommand(`analyze --path "${workspacePath}" --save-findings`);
        await this.parseAnalysisOutput(output, workspacePath);
    }

    async learnPatterns(threshold: number): Promise<{ patternsFound: number; patchesGenerated: number }> {
        const output = await this.runCommand(`learn --threshold ${threshold}`);
        
        // Parse output for pattern count
        const patternsMatch = output.match(/Patterns Identified:\s+(\d+)/);
        const patchesMatch = output.match(/Patches Generated:\s+(\d+)/);
        
        const patternsFound = patternsMatch ? parseInt(patternsMatch[1]) : 0;
        const patchesGenerated = patchesMatch ? parseInt(patchesMatch[1]) : 0;

        await this.loadPatterns();

        return { patternsFound, patchesGenerated };
    }

    async scaffoldProject(name: string, author: string, description: string): Promise<string> {
        const workspacePath = this.getWorkspacePath();
        const projectPath = path.join(workspacePath, name);
        
        await this.runCommand(
            `scaffold --name "${name}" --author "${author}" --description "${description}"`
        );
        
        return projectPath;
    }

    async getStats(): Promise<Stats> {
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
        } catch (error) {
            // Fallback to cached data
            return {
                totalFindings: this.findings.length,
                totalPatterns: this.patterns.length,
                totalImprovements: 0,
                learningRate: 0
            };
        }
    }

    async generateHandoff(filePath: string): Promise<string> {
        const config = vscode.workspace.getConfiguration('ultrathink');
        const profile = config.get<string>('projectProfile') || 'auto';
        
        let cmd = `handoff --path "${filePath}"`;
        if (profile !== 'auto') {
            cmd += ` --profile ${profile}`;
        }
        
        const output = await this.runCommand(cmd);
        return output.trim();
    }

    getFindings(): Finding[] {
        return this.findings;
    }

    getPatterns(): Pattern[] {
        return this.patterns;
    }

    private async parseAnalysisOutput(output: string, basePath: string): Promise<void> {
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

    private async loadPatterns(): Promise<void> {
        // Load patterns from knowledge base
        // This would query the SQLite database in production
        this.patterns = [];
    }
}
