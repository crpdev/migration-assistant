import * as vscode from 'vscode';
import { MigrationOrchestrator } from './migrationOrchestrator';
import { MigrationLogger } from './migrationLogger';
import { MigrationStepsProvider } from './migrationStepsProvider';
import { MigrationReportProvider } from './migrationReportProvider';

export async function activate(context: vscode.ExtensionContext) {
    // Register the migration steps provider
    const migrationStepsProvider = new MigrationStepsProvider();
    vscode.window.registerTreeDataProvider('migrationSteps', migrationStepsProvider);

    // Register the migration report provider
    const migrationReportProvider = new MigrationReportProvider();
    vscode.window.registerTreeDataProvider('migrationReport', migrationReportProvider);

    // Register the start migration command
    let disposable = vscode.commands.registerCommand('java-migration-assistant.startMigration', async () => {
        try {
            // Get the workspace folder
            const workspaceFolders = vscode.workspace.workspaceFolders;
            if (!workspaceFolders || workspaceFolders.length === 0) {
                vscode.window.showErrorMessage('Please open a workspace folder first');
                return;
            }

            const projectPath = workspaceFolders[0].uri.fsPath;

            // Check if it's a Maven project
            const pomPath = vscode.Uri.joinPath(workspaceFolders[0].uri, 'pom.xml');
            try {
                await vscode.workspace.fs.stat(pomPath);
            } catch {
                vscode.window.showErrorMessage('No pom.xml found in the workspace. Please open a Maven project.');
                return;
            }

            // Initialize the migration orchestrator
            const orchestrator = new MigrationOrchestrator(projectPath);
            
            // Show progress
            await vscode.window.withProgress({
                location: vscode.ProgressLocation.Notification,
                title: "Java Migration Assistant",
                cancellable: true
            }, async (progress, token) => {
                token.onCancellationRequested(() => {
                    vscode.window.showInformationMessage('Migration cancelled by user');
                });

                // Start the migration process
                progress.report({ message: 'Starting migration process...' });
                
                const result = await orchestrator.run_migration(projectPath);
                
                if (result.success) {
                    vscode.window.showInformationMessage('Migration completed successfully!');
                    // Update the migration steps and report views
                    migrationStepsProvider.refresh();
                    migrationReportProvider.refresh();
                    
                    // Open the report in a new editor
                    const reportUri = vscode.Uri.file(result.report_path);
                    const doc = await vscode.workspace.openTextDocument(reportUri);
                    await vscode.window.showTextDocument(doc, { preview: false });
                } else {
                    vscode.window.showErrorMessage(`Migration failed: ${result.message || result.error}`);
                    if (result.reasoning) {
                        // Show reasoning in a new editor
                        const content = new vscode.MarkdownString(result.reasoning);
                        const doc = await vscode.workspace.openTextDocument({
                            content: content.value,
                            language: 'markdown'
                        });
                        await vscode.window.showTextDocument(doc, { preview: false });
                    }
                }
            });
        } catch (error) {
            vscode.window.showErrorMessage(`An error occurred: ${error.message}`);
        }
    });

    context.subscriptions.push(disposable);
}

export function deactivate() {} 