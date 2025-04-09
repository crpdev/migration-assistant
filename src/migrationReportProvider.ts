import * as vscode from 'vscode';
import * as fs from 'fs';
import * as path from 'path';

export class MigrationReportItem extends vscode.TreeItem {
    constructor(
        public readonly label: string,
        public readonly content: string,
        public readonly collapsibleState: vscode.TreeItemCollapsibleState = vscode.TreeItemCollapsibleState.None
    ) {
        super(label, collapsibleState);
        this.tooltip = content;
    }
}

export class MigrationReportProvider implements vscode.TreeDataProvider<MigrationReportItem> {
    private _onDidChangeTreeData: vscode.EventEmitter<MigrationReportItem | undefined | null | void> = new vscode.EventEmitter<MigrationReportItem | undefined | null | void>();
    readonly onDidChangeTreeData: vscode.Event<MigrationReportItem | undefined | null | void> = this._onDidChangeTreeData.event;

    private reportItems: MigrationReportItem[] = [];
    private reportPath: string | undefined;

    constructor() {}

    refresh(): void {
        this._onDidChangeTreeData.fire();
    }

    setReportPath(path: string) {
        this.reportPath = path;
        this.loadReport();
    }

    private async loadReport() {
        if (!this.reportPath || !fs.existsSync(this.reportPath)) {
            this.reportItems = [];
            this.refresh();
            return;
        }

        try {
            const content = await fs.promises.readFile(this.reportPath, 'utf8');
            const parser = new DOMParser();
            const doc = parser.parseFromString(content, 'text/html');
            
            this.reportItems = [];
            
            // Extract project info
            const projectPath = doc.querySelector('p:contains("Project:")')?.textContent;
            if (projectPath) {
                this.reportItems.push(new MigrationReportItem(
                    'Project',
                    projectPath.replace('Project:', '').trim()
                ));
            }

            // Extract migration steps
            const steps = doc.querySelectorAll('.step');
            steps.forEach((step, index) => {
                const title = step.querySelector('h3')?.textContent || `Step ${index + 1}`;
                const details = Array.from(step.querySelectorAll('.details p'))
                    .map(p => p.textContent)
                    .join('\n');
                
                this.reportItems.push(new MigrationReportItem(
                    title,
                    details,
                    vscode.TreeItemCollapsibleState.Collapsed
                ));
            });

            this.refresh();
        } catch (error) {
            vscode.window.showErrorMessage(`Failed to load migration report: ${error.message}`);
            this.reportItems = [];
            this.refresh();
        }
    }

    getTreeItem(element: MigrationReportItem): vscode.TreeItem {
        return element;
    }

    getChildren(element?: MigrationReportItem): Thenable<MigrationReportItem[]> {
        if (!element) {
            return Promise.resolve(this.reportItems);
        }
        return Promise.resolve([]);
    }
} 