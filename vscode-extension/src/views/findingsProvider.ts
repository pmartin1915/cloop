import * as vscode from 'vscode';
import { UltrathinkService, Finding } from '../ultrathinkService';

export class FindingsProvider implements vscode.TreeDataProvider<FindingItem> {
    private _onDidChangeTreeData: vscode.EventEmitter<FindingItem | undefined | null | void> = new vscode.EventEmitter<FindingItem | undefined | null | void>();
    readonly onDidChangeTreeData: vscode.Event<FindingItem | undefined | null | void> = this._onDidChangeTreeData.event;

    constructor(private ultrathinkService: UltrathinkService) {}

    refresh(): void {
        this._onDidChangeTreeData.fire();
    }

    getTreeItem(element: FindingItem): vscode.TreeItem {
        return element;
    }

    getChildren(element?: FindingItem): Thenable<FindingItem[]> {
        if (!element) {
            const findings = this.ultrathinkService.getFindings();
            
            if (findings.length === 0) {
                return Promise.resolve([
                    new FindingItem('No findings yet', 'Run "Analyze File" to start', vscode.TreeItemCollapsibleState.None, 'info')
                ]);
            }

            const grouped = this.groupBySeverity(findings);
            const severityOrder = ['critical', 'high', 'medium', 'low', 'info'];
            const items: FindingItem[] = [];

            for (const severity of severityOrder) {
                const severityFindings = grouped[severity];
                if (severityFindings && severityFindings.length > 0) {
                    const item = new FindingItem(
                        `${severity.toUpperCase()} (${severityFindings.length})`,
                        '',
                        vscode.TreeItemCollapsibleState.Collapsed,
                        severity
                    );
                    item.findings = severityFindings;
                    items.push(item);
                }
            }

            return Promise.resolve(items);
        } else {
            if (element.findings) {
                return Promise.resolve(
                    element.findings.map(f => {
                        const item = new FindingItem(
                            f.description,
                            f.suggestion,
                            vscode.TreeItemCollapsibleState.None,
                            f.severity
                        );
                        item.command = {
                            command: 'vscode.open',
                            title: 'Open File',
                            arguments: [vscode.Uri.file(f.file), { selection: new vscode.Range(f.line, 0, f.line, 0) }]
                        };
                        return item;
                    })
                );
            }
            return Promise.resolve([]);
        }
    }

    private groupBySeverity(findings: Finding[]): Record<string, Finding[]> {
        const grouped: Record<string, Finding[]> = {};
        
        for (const finding of findings) {
            if (!grouped[finding.severity]) {
                grouped[finding.severity] = [];
            }
            grouped[finding.severity].push(finding);
        }

        return grouped;
    }
}

class FindingItem extends vscode.TreeItem {
    findings?: Finding[];

    constructor(
        public readonly label: string,
        public description: string,
        public readonly collapsibleState: vscode.TreeItemCollapsibleState,
        private severity: string
    ) {
        super(label, collapsibleState);
        this.tooltip = description;
        this.description = description;
        this.iconPath = this.getIcon(severity);
    }

    private getIcon(severity: string): vscode.ThemeIcon {
        const iconMap: Record<string, string> = {
            critical: 'error',
            high: 'warning',
            medium: 'info',
            low: 'circle-outline',
            info: 'info'
        };
        return new vscode.ThemeIcon(iconMap[severity] || 'circle-outline');
    }
}
