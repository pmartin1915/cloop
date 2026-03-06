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
exports.FindingsProvider = void 0;
const vscode = __importStar(require("vscode"));
class FindingsProvider {
    constructor(ultrathinkService) {
        this.ultrathinkService = ultrathinkService;
        this._onDidChangeTreeData = new vscode.EventEmitter();
        this.onDidChangeTreeData = this._onDidChangeTreeData.event;
    }
    refresh() {
        this._onDidChangeTreeData.fire();
    }
    getTreeItem(element) {
        return element;
    }
    getChildren(element) {
        if (!element) {
            const findings = this.ultrathinkService.getFindings();
            if (findings.length === 0) {
                return Promise.resolve([
                    new FindingItem('No findings yet', 'Run "Analyze File" to start', vscode.TreeItemCollapsibleState.None, 'info')
                ]);
            }
            const grouped = this.groupBySeverity(findings);
            const severityOrder = ['critical', 'high', 'medium', 'low', 'info'];
            const items = [];
            for (const severity of severityOrder) {
                const severityFindings = grouped[severity];
                if (severityFindings && severityFindings.length > 0) {
                    const item = new FindingItem(`${severity.toUpperCase()} (${severityFindings.length})`, '', vscode.TreeItemCollapsibleState.Collapsed, severity);
                    item.findings = severityFindings;
                    items.push(item);
                }
            }
            return Promise.resolve(items);
        }
        else {
            if (element.findings) {
                return Promise.resolve(element.findings.map(f => {
                    const item = new FindingItem(f.description, f.suggestion, vscode.TreeItemCollapsibleState.None, f.severity);
                    item.command = {
                        command: 'vscode.open',
                        title: 'Open File',
                        arguments: [vscode.Uri.file(f.file), { selection: new vscode.Range(f.line, 0, f.line, 0) }]
                    };
                    return item;
                }));
            }
            return Promise.resolve([]);
        }
    }
    groupBySeverity(findings) {
        const grouped = {};
        for (const finding of findings) {
            if (!grouped[finding.severity]) {
                grouped[finding.severity] = [];
            }
            grouped[finding.severity].push(finding);
        }
        return grouped;
    }
}
exports.FindingsProvider = FindingsProvider;
class FindingItem extends vscode.TreeItem {
    constructor(label, description, collapsibleState, severity) {
        super(label, collapsibleState);
        this.label = label;
        this.description = description;
        this.collapsibleState = collapsibleState;
        this.severity = severity;
        this.tooltip = description;
        this.description = description;
        this.iconPath = this.getIcon(severity);
    }
    getIcon(severity) {
        const iconMap = {
            critical: 'error',
            high: 'warning',
            medium: 'info',
            low: 'circle-outline',
            info: 'info'
        };
        return new vscode.ThemeIcon(iconMap[severity] || 'circle-outline');
    }
}
//# sourceMappingURL=findingsProvider.js.map