import * as vscode from 'vscode';
import { UltrathinkService } from '../ultrathinkService';

export class StatsProvider implements vscode.TreeDataProvider<StatItem> {
    private _onDidChangeTreeData: vscode.EventEmitter<StatItem | undefined | null | void> = new vscode.EventEmitter<StatItem | undefined | null | void>();
    readonly onDidChangeTreeData: vscode.Event<StatItem | undefined | null | void> = this._onDidChangeTreeData.event;

    constructor(private ultrathinkService: UltrathinkService) {}

    refresh(): void {
        this._onDidChangeTreeData.fire();
    }

    getTreeItem(element: StatItem): vscode.TreeItem {
        return element;
    }

    async getChildren(element?: StatItem): Promise<StatItem[]> {
        if (element) {
            return [];
        }

        try {
            const stats = await this.ultrathinkService.getStats();

            return [
                new StatItem('Findings', stats.totalFindings.toString(), 'search', 'Total code issues found'),
                new StatItem('Patterns', stats.totalPatterns.toString(), 'lightbulb', 'Recurring patterns identified'),
                new StatItem('Improvements', stats.totalImprovements.toString(), 'check', 'Patches ready to apply'),
                new StatItem('Learning Rate', `${stats.learningRate.toFixed(1)}%`, 'graph', 'Effectiveness of learning')
            ];
        } catch (error) {
            return [
                new StatItem('Error', 'Failed to load stats', 'error', String(error))
            ];
        }
    }
}

class StatItem extends vscode.TreeItem {
    constructor(
        public readonly label: string,
        private value: string,
        private icon: string,
        private tooltipText?: string
    ) {
        super(label, vscode.TreeItemCollapsibleState.None);
        this.description = value;
        this.iconPath = new vscode.ThemeIcon(icon);
        this.tooltip = tooltipText || `${label}: ${value}`;
    }
}
