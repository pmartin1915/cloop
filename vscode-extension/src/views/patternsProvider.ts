import * as vscode from 'vscode';
import { UltrathinkService, Pattern } from '../ultrathinkService';

export class PatternsProvider implements vscode.TreeDataProvider<PatternItem> {
    private _onDidChangeTreeData: vscode.EventEmitter<PatternItem | undefined | null | void> = new vscode.EventEmitter<PatternItem | undefined | null | void>();
    readonly onDidChangeTreeData: vscode.Event<PatternItem | undefined | null | void> = this._onDidChangeTreeData.event;

    constructor(private ultrathinkService: UltrathinkService) {}

    refresh(): void {
        this._onDidChangeTreeData.fire();
    }

    getTreeItem(element: PatternItem): vscode.TreeItem {
        return element;
    }

    getChildren(element?: PatternItem): Thenable<PatternItem[]> {
        if (element) {
            return Promise.resolve([]);
        }

        const patterns = this.ultrathinkService.getPatterns();
        
        if (patterns.length === 0) {
            return Promise.resolve([
                new PatternItem('No patterns learned yet', 'Run "Learn Patterns" to start', 0, 'unknown')
            ]);
        }

        const sorted = patterns.sort((a, b) => b.frequency - a.frequency);

        return Promise.resolve(
            sorted.map(p => new PatternItem(
                p.description,
                `${p.category} • ${p.frequency}x`,
                p.frequency,
                p.category
            ))
        );
    }
}

class PatternItem extends vscode.TreeItem {
    constructor(
        public readonly label: string,
        public description: string,
        private frequency: number,
        private category: string
    ) {
        super(label, vscode.TreeItemCollapsibleState.None);
        this.tooltip = `${label}\n${description}`;
        this.description = description;
        this.iconPath = this.getIcon(category);
    }

    private getIcon(category: string): vscode.ThemeIcon {
        const iconMap: Record<string, string> = {
            bug: 'bug',
            security: 'shield',
            quality: 'star',
            performance: 'zap',
            style: 'paintcan'
        };
        return new vscode.ThemeIcon(iconMap[category] || 'lightbulb');
    }
}
